from sqlmodel import select

from typing import Annotated

from fastapi import HTTPException

from datetime import datetime, timedelta, timezone
from fastapi import Depends
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jwt.exceptions import InvalidTokenError
from passlib.context import CryptContext
from pydantic import BaseModel, ValidationError
from sqlmodel import Session, SQLModel, create_engine
from typing import Annotated
import jwt
from sqlmodel import Field, SQLModel, select


sqlite_url = "postgresql+psycopg2://postgres:postgres@localhost:5432"

engine = create_engine(sqlite_url)


def get_session():
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_session)]


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


def create_admin_user():
    session = next(get_session())
    admin_exists = get_user(session, "admin")
    if admin_exists:
        return
    admin_create = UserCreate(
        username="admin", email="admin@admin.admin", is_admin=True, password="admin123"
    )
    db_user = User.model_validate(
        admin_create,
        update={"hashed_password": get_password_hash(admin_create.password)},
    )
    session.add(db_user)
    session.commit()
    session.refresh(db_user)


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

TokenDep = Annotated[str, Depends(oauth2_scheme)]


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: int


def get_token_data(token, credentials_exception):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        id: int = payload.get("sub")
        # if username is None:
        #     raise credentials_exception
        return TokenData(id=id)
    except InvalidTokenError:
        raise credentials_exception


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def create_access_token(data, expires_delta: timedelta | None = None):
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)

    to_encode = {"exp": expire, "sub": data}

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def authenticate_user(session: SessionDep, username: str, password: str):
    user = get_user(session, username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


ACCESS_TOKEN_EXPIRE_MINUTES = 30


class UserBase(SQLModel):
    username: str = Field(unique=True, index=True, max_length=32)
    email: str = Field(unique=True)
    is_admin: bool = Field(default=False)


class User(UserBase, table=True):
    id: int = Field(primary_key=True, default=None)
    username: str
    hashed_password: str


class UserPublic(UserBase):
    username: str


class UserCreate(UserBase):
    password: str = Field(min_length=8)


class UserUpdate(UserBase):
    username: str | None = Field(default=None, max_length=32)  # type: ignore
    password: str | None = Field(default=None, min_length=8)


def get_user_by_email(session, email):
    statement = select(User).where(User.email == email)
    session_user = session.exec(statement).first()
    return session_user


def get_user(session, username):
    statement = select(User).where(User.username == username)
    session_user = session.exec(statement).first()
    return session_user


def get_current_user(session: SessionDep, token: TokenDep) -> User:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        token_data = TokenData(id=payload["sub"])
    except (InvalidTokenError, ValidationError):
        raise HTTPException(
            status_code=403,
            detail="Could not validate credentials",
        )
    user = session.get(User, token_data.id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    if not user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return user


CurrentUser = Annotated[User, Depends(get_current_user)]

SECRET_KEY = "3402751aab4a5d55d02e6e812db0d32d4b3942dae74f6648fe7b630e3df043ec"

ALGORITHM = "HS256"
