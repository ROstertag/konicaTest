import os
import cv2
import json
from flask import Flask, flash, request, redirect, render_template
from werkzeug.utils import secure_filename
from nats.aio.client import Client as NATS
from nats.aio.errors import ErrConnectionClosed, ErrTimeout, ErrNoServers

app = Flask(__name__)

NATS_ADDRESS = "nats-0.nats.default.svc:4222"

app.secret_key = "secret key"
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

# Get current path
path = os.getcwd()
# file Upload
UPLOAD_FOLDER = os.path.join(path, 'uploads')

# Make directory if uploads is not exists
if not os.path.isdir(UPLOAD_FOLDER):
    os.mkdir(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Allowed extension you can set your own, probably more should be allowed
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])


def allowed_file(filename) -> str:
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


async def process_files(files, nc) -> None:
    for file in files:
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            try:
                # save file locally
                path_to_file = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(path_to_file)

                # read file as img
                img = cv2.imread(path_to_file, -1)

                # publish image to nats with name and data
                await nc.publish("pictures", json.dumps({"filename": filename, "img": img.tolist()}).encode())

                # deletes local file
                os.remove(path_to_file)

                flash("File {} sent ".format(filename))

            except ErrConnectionClosed as e:
                flash("Connection closed prematurely.")
                break
            except ErrTimeout as e:
                flash("Timeout occured when publishing msg filename={}: {}".format(
                    filename, e))
        else:
            flash("Wrong type of file {}. Allowed only \'png\', \'jpg\', \'jpeg\', \'gif\'".format(file.filename))


@app.route('/')
def upload_form():
    return render_template('upload_form.html')


@app.route('/', methods=['POST'])
async def upload_file():
    if request.method == 'POST':

        if 'files[]' not in request.files:
            flash('No file part')
            return redirect(request.url)

        # get files list for upload
        files = request.files.getlist('files[]')

        if len(files) > 20:
            flash('Too many files for upload')
            return redirect(request.url)

        nc = NATS()

        try:
            # open nats client connection
            await nc.connect(NATS_ADDRESS)
        except ErrConnectionClosed as e:
            flash("Connection closed prematurely. Error: {} ".format(e))
        except ErrTimeout as e:
            flash("Connection Timeout occured. Error: {} ".format(e))
        except ErrNoServers as e:
            flash("Problem with connection servers. Error: {} ".format(e))

        await process_files(files, nc)

        # Here can come routine for displaying saved files from writer

        await nc.close()

        return redirect('/')


if __name__ == "__main__":
    app.run(host='127.0.0.1',port=2222,debug=False,threaded=True)
