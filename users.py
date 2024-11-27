from fastapi import Query, APIRouter

from utils import *

router = APIRouter()


@router.get("/", response_model=list[UserPublic])
def read_users(
    current_user: CurrentUser,
    session: SessionDep,
    offset: int = 0,
    limit: Annotated[int, Query(le=100)] = 100,
):
    if not current_user.is_admin:
        raise HTTPException(status_code=401, detail="You're not an admin")
    users = session.exec(select(User).offset(offset).limit(limit)).all()
    return users


@router.post("/", response_model=UserPublic)
def create_user(user_create: UserCreate, session: SessionDep):
    user_exists = get_user(session, user_create.username)
    if user_exists:
        raise HTTPException(status_code=400, detail="username already exists")
    email_exists = get_user_by_email(session, user_create.email)
    if email_exists:
        raise HTTPException(status_code=400, detail="email already exists")
    db_user = User.model_validate(
        user_create, update={"hashed_password": get_password_hash(user_create.password)}
    )
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user


@router.get("/me", response_model=UserPublic)
def read_user_me(current_user: CurrentUser):
    """
    Get current user.
    """
    return current_user


@router.get("/{user_id}", response_model=UserPublic)
def read_user(user_id: int, session: SessionDep):
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.delete("/{user_id}")
def delete_user(user_id: int, current_user: CurrentUser, session: SessionDep):
    if current_user.id != user_id and not current_user.is_admin:
        raise HTTPException(
            status_code=401, detail="You are not this user and you are not an admin"
        )

    user = session.get(User, user_id)
    if user:
        session.delete(user)
        session.commit()
    return {"ok": True}


@router.patch("/{user_id}", response_model=UserPublic)
def update_user(
    current_user: CurrentUser,
    user_id: int,
    user_update: UserUpdate,
    session: SessionDep,
):
    if current_user.id != user_id and not current_user.is_admin:
        raise HTTPException(
            status_code=401, detail="You are not this user and you are not an admin"
        )

    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    user_data = user_update.model_dump(exclude_unset=True)
    user.sqlmodel_update(user_data)
    session.add(user)
    session.commit()
    session.refresh(user)
    return user
