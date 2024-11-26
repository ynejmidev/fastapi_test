import json
import requests
from faker import Faker


def fake_users(number=10):
    fake = Faker()
    users = []
    for _ in range(number):
        users.append(
            {
                "username": fake.user_name(),
                "password": fake.password(),
                "full_name": fake.name(),
                "email": fake.email(),
            }
        )
    return users


users = fake_users()  # unique?


def test_add_users():
    def request(user):
        return requests.post(
            "http://localhost:8000/users/",
            data=json.dumps(user),
            headers={"accept": "application/json", "Content-Type": "application/json"},
        )

    res_map = map(
        request,
        users,
    )
    for res, user in zip(res_map, users):
        assert res.status_code == 200
        assert res.json()['username'] == user['username']


def test_main():
    data = users[0]
    tok = requests.post("http://localhost:8000/token", data)
    res = tok.json()

    assert tok.status_code == 200
    assert res["token_type"].lower() == "bearer"

    me = requests.get(
        "http://localhost:8000/users/me",
        headers={"Authorization": "Bearer " + res["access_token"]},
    )

    assert me.status_code == 200
