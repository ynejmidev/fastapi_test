import requests

from users import fake_users_db


def test_main():
    data = {
        "grant_type": "password",
        "username": "johndoe",
        "password": "secret",
    }
    tok = requests.post("http://localhost:8000/token", data)
    res = tok.json()

    print(res["access_token"])

    assert tok.status_code == 200
    assert res["token_type"].lower() == "bearer"
    assert len(res["access_token"]) == 127

    me = requests.get(
        "http://localhost:8000/users/me",
        headers={
            "Authorization": "Bearer " + res["access_token"]
        },
    )

    [expected] = fake_users_db.values()

    assert me.status_code == 200
    assert me.json() == expected
