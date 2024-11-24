from typing import Annotated

from fastapi import Depends, FastAPI

from utils import get_current_user, User

app = FastAPI()


@app.get("/users/me")
async def read_users_me(current_user: Annotated[User, Depends(get_current_user)]):
    return current_user
