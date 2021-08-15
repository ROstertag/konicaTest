FROM python:3.7-slim

WORKDIR /app

ADD . /app

RUN apt-get update && apt-get install -y libpq-dev libgl1-mesa-glx gcc libglib2.0-0 libsm6 libxrender1 libxext6 vim
# need gcc to compile psycopg2
RUN pip3 install psycopg2~=2.6
RUN apt-get autoremove -y gcc
RUN pip install --trusted-host pypi.python.org -r requirements.txt

EXPOSE 2222

CMD [ "python3", "file_upload.py"]
