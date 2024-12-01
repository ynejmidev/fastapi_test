from sqlmodel import Field, Relationship, SQLModel


class UserBase(SQLModel):
    username: str = Field(unique=True, index=True, max_length=32)
    email: str = Field(unique=True, default=None)
    is_admin: bool = Field(default=False)


class User(UserBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    username: str
    hashed_password: str
    propriete: list["Propriete"] = Relationship(back_populates="user")


class UserPublic(UserBase):
    id: int


class UserCreate(UserBase):
    password: str = Field(min_length=8)


class UserUpdate(UserBase):
    username: str | None = Field(default=None, max_length=32)  # type: ignore
    password: str | None = Field(default=None, min_length=8)
