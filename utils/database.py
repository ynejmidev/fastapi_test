from datetime import datetime
from sqlmodel import SQLModel, select

from models.property import Adresse, Agent, Propriete
from models.users import User, UserCreate
from utils.other import get_password_hash, get_session, get_user, engine


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


def create_admin_user():
    session = next(get_session())
    admin_exists = get_user(session, "admin")
    if admin_exists:
        return
    admin_create = UserCreate(
        username="admin",
        email="admin@admin.admin",
        is_admin=True,
        password="admin123",
    )
    db_user = User.model_validate(
        admin_create,
        update={
            "hashed_password": get_password_hash(admin_create.password),
        },
    )
    session.add(db_user)
    session.commit()
    agent = Agent(nom="aziz", telephone="0000", email="aziz@aziz.aziz")
    new_property = Propriete(
        titre="Belle maison familiale",
        description="Belle maison familiale",
        type="Belle maison familiale",
        prix=202,
        statut="Belle maison familiale",
        devise="Belle maison familiale",
        chambres=2000,
        salles_de_bain=0,
        ensoleillement="Belle maison familiale",
        orientation_soleil="Belle maison familiale",
        date_ajout=datetime.now(),
        date_construction=datetime.now(),
        agent=agent,
        user=db_user,
    )
    address = Adresse(
        propriete=new_property,
        rue="malika",
        ville="casa",
        region="tanger",
        code_postal="11000",
        pays="casa",
    )
    session.add_all([new_property, db_user, address, agent])
    session.commit()

    session.refresh(db_user)
