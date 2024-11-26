import requests


def test_main():
    data = {
        "grant_type": "password",
        "username": "johndoe",
        "password": "secret12",
    }
    tok = requests.post("http://localhost:8000/token", data)
    res = tok.json()

    assert tok.status_code == 200
    assert res["token_type"].lower() == "bearer"

    me = requests.get(
        "http://localhost:8000/users/me",
        headers={"Authorization": "Bearer " + res["access_token"]},
    )

    assert me.status_code == 200
