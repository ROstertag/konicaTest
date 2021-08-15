import os
import cv2
import json
import asyncio
from flask import Flask, flash, request, redirect, render_template
from werkzeug.utils import secure_filename
from nats.aio.client import Client as NATS
from nats.aio.errors import ErrConnectionClosed, ErrTimeout, ErrNoServers

app=Flask(__name__)

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


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


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

        nc = NATS()

        try:
            # open nats client connection
            await nc.connect("nats-0.nats.default.svc:4222")
        except ErrConnectionClosed as e:
            print("Connection closed prematurely. Error: %s ", e)
        except ErrTimeout as e:
            print("Connection Timeout occured. Error: %s ", e)
        except ErrNoServers as e:
            print("Problem with connection servers. Error: %s ", e)

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

        # tu pride subscribe a flash routina na spracovane subory


        await nc.close()

        flash('File(s) successfully uploaded')
        return redirect('/')


if __name__ == "__main__":
    app.run(host='0.0.0.0',port=2222,debug=False,threaded=True)
