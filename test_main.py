import time
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
                "id": 0,
            }
        )
    return users


users = fake_users()  # unique?


class Admin:
    token = ""
    cred = {"username": "admin", "password": "admin123"}


admin = Admin()


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

    class bcolors:
        HEADER = "\033[95m"
        OKBLUE = "\033[94m"
        OKCYAN = "\033[96m"
        OKGREEN = "\033[92m"
        WARNING = "\033[93m"
        FAIL = "\033[91m"
        ENDC = "\033[0m"
        BOLD = "\033[1m"
        UNDERLINE = "\033[4m"

    print(
        bcolors.OKGREEN, "START", bcolors.ENDC
    )  # .2sec/req... HOWWWWWWW what? localhost??
    start_time = time.perf_counter()

    for res, user in zip(res_map, users):
        assert res.status_code == 200
        user["id"] = res.json()["id"]
        assert res.json()["username"] == user["username"]

    process_time = time.perf_counter() - start_time
    print(bcolors.OKCYAN, process_time, bcolors.ENDC)

    # for user in users:
    #     print(user["id"])

    # test duplicate (email & password are unique)
    dup_res = request(users[0])
    assert dup_res.status_code == 400


def test_admin_token():
    res = requests.post(
        "http://localhost:8000/token",
        admin.cred,
    )
    [admin.token, type] = res.json().values()

    assert res.status_code == 200
    assert type == "bearer"


def test_admin_get_me():
    admin_res = requests.get(
        "http://localhost:8000/users/me",
        headers={"Authorization": "Bearer " + admin.token},
    )

    assert admin_res.status_code == 200


def test_admin_get_users():
    res = requests.get(
        "http://localhost:8000/users/",
        headers={"Authorization": "Bearer " + admin.token},
    )
    # print(res.json())


def test_admin_update():
    url = f"http://localhost:8000/users/{users[0]['id']}"
    before_res = requests.get(
        url,
        headers={"Authorization": "Bearer " + admin.token},
    )

    update_res = requests.patch(
        url,
        headers={
            "Authorization": "Bearer " + admin.token,
            "accept": "application/json",
            "Content-Type": "application/json",
        },
        data=json.dumps({"username": "aaaaaaaaa"}),
    )
    assert before_res.json()["username"] != update_res.json()["username"]
    # print(update_res.json())


def test_admin_delete():
    url = f"http://localhost:8000/users/{users[0]['id']}"
    before_res = requests.get(
        url,
        headers={"Authorization": "Bearer " + admin.token},
    )

    requests.delete(
        url,
        headers={"Authorization": "Bearer " + admin.token},
    )

    update_res = requests.get(
        url,
        headers={"Authorization": "Bearer " + admin.token},
    )
    assert before_res.status_code == 200
    assert update_res.status_code == 404
