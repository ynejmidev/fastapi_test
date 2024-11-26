from sqlmodel import Field, SQLModel, select


class UserBase(SQLModel):
    username: str = Field(unique=True, index=True, max_length=32)
    email: str
    is_admin: bool = Field(default=False)


class User(UserBase, table=True):
    id: int = Field(primary_key=True, default=None)
    username: str
    hashed_password: str
    is_admin: bool = Field(default=False)
    is_active: bool = Field(default=True)


class UserPublic(UserBase):
    id: int
    username: str


class UserCreate(UserBase):
    password: str = Field(min_length=8)


class UserUpdate(UserBase):
    email: str
    username: str


def get_user(session, username):
    statement = select(User).where(User.username == username)
    session_user = session.exec(statement).first()
    return session_user
