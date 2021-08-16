import pytest
import asyncio
from processor.process import convert_rgb_to_names
from processor.process import run
from mock import patch, Mock, MagicMock
import io
import json
import flask
from werkzeug.datastructures import ImmutableMultiDict

import requests


def test_home_page_server_not_running():
    app = flask.Flask(__name__)

    # Create a test client using the Flask application configured for testing
    with app.test_client() as test_client:
        response = test_client.get('/')
        assert response.status_code == 404


def test_get_home_page(client):
    response = client.get("/")
    assert response.status_code == 200


def test_post_home_page_no_file(client):
    mimetype = 'application/json'
    headers = {
        'Content-Type': mimetype,
        'Accept': mimetype
    }
    files = ImmutableMultiDict([])

    response = client.post("/", data={
            'files': files,
        }, headers=headers)
    assert response.status_code == 302


def test_post_home_page(client):
    mimetype = 'application/json'
    headers = {
        'Content-Type': mimetype,
        'Accept': mimetype
    }
    request = MagicMock()
    request.FILES.keys.return_value = ['file_id']
    request.FILES.getlist.return_value = ['file'] * 12
    data = dict(files=[(io.BytesIO(b"this is a test"), 'test.pdf')], follow_redirects=True)
    # response = requests.post("http://localhost/", files=files)
    response = client.post("/", headers=headers, data=data)
    assert response.status_code == 302
