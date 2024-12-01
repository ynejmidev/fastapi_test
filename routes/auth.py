from datetime import timedelta
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm

from models.auth import Token
from utils.other import (
    ACCESS_TOKEN_EXPIRE_MINUTES,
    authenticate_user,
    SessionDep,
    create_access_token,
)
from utils.database import create_admin_user, create_db_and_tables

router = APIRouter()


@router.on_event("startup")
def on_startup():
    create_db_and_tables()
    create_admin_user()


@router.post("/token")
async def login_for_access_token(
    session: SessionDep,
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
) -> Token:
    user = authenticate_user(session, form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=401, detail="Incorrect username or password")
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(user.id, access_token_expires)
    return Token(access_token=access_token, token_type="bearer")
