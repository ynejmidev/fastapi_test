from fastapi import APIRouter
from sqlmodel import func

from models.property import *
from utils.other import *

router = APIRouter()


@router.get("/", response_model=list[Propriete])
def read_property(
    session: SessionDep, current_user: CurrentUser, skip: int = 0, limit: int = 100
):
    try:
        if current_user.is_admin:
            count_statement = select(func.count()).select_from(Propriete)
            count = session.exec(count_statement).one()
            print(count)
            statement = select(Propriete).offset(skip).limit(limit)
            property = session.exec(statement).all()
            print(property)
        else:
            count_statement = (
                select(func.count())
                .select_from(Propriete)
                .where(Propriete.user_id == current_user.id)
            )
            count = session.exec(count_statement).one()
            statement = (
                select(Propriete)
                .where(Propriete.user_id == current_user.id)
                .offset(skip)
                .limit(limit)
            )
            property = session.exec(statement).all()
        return property
    except Exception as e:
        print("opzi:", e)


@router.get("/{id}", response_model=Propriete)
def read_property_one(session: SessionDep, current_user: CurrentUser, id: int):

    property = session.get(Propriete, id)
    if not property:
        raise HTTPException(status_code=404, detail="Propriete not found")
    if not current_user.is_admin and (property.user_id != current_user.id):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    return property


@router.post("/", response_model=Propriete)
def create_property(
    *, session: SessionDep, current_user: CurrentUser, property_in: ProprieteCreate
):

    try:
        property = Propriete.model_validate(
            property_in, update={"user_id": current_user.id}
        )
        session.add(property)
        session.commit()
        session.refresh(property)
        return property
    except Exception as e:
        print(e)
        raise HTTPException(status_code=400, detail="property not unique?")


@router.put("/{id}", response_model=Propriete)
def update_property(
    *,
    session: SessionDep,
    current_user: CurrentUser,
    id: int,
    property_in: ProprieteUpdate,
):

    property = session.get(Propriete, id)
    if not property:
        raise HTTPException(status_code=404, detail="Propriete not found")
    if not current_user.is_admin and (property.user_id != current_user.id):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    update_dict = property_in.model_dump(exclude_unset=True)
    property.sqlmodel_update(update_dict)
    session.add(property)
    session.commit()
    session.refresh(property)
    return property


@router.delete("/{id}")
def delete_property(session: SessionDep, current_user: CurrentUser, id: int):

    property = session.get(Propriete, id)
    if not property:
        raise HTTPException(status_code=404, detail="Propriete not found")
    if not current_user.is_admin and (property.user_id != current_user.id):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    session.delete(property)
    session.commit()
    return {"ok": True}
