import pytest
import requests


def test_token():
    data = {
        "grant_type": "password",
        "username": "johndoe",
        "password": "secret",
    }
    x = requests.post("http://localhost:8000/token", data)
    assert x.status_code == 200
