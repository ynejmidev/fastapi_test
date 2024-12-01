# {
#   "propriete": {
#     "id": "1",
#     "titre": "Belle maison familiale",
#     "description": "Une maison familiale spacieuse et moderne avec 3 chambres, un grand jardin et un garage.",
#     "type": "maison",  // Valeurs possibles : maison, appartement, condo, terrain, etc.
#     "statut": "à vendre",  // Valeurs possibles : à vendre, à louer
#     "prix": 250000,  // Prix dans votre devise locale
#     "devise": "Dirham",
#     "adresse": {
#       "rue": "123 rue Principale",
#       "ville": "Kenitra",
#       "region": "rabat-kenitra-sale",
#       "code_postal": "75001",
#       "pays": "maroc"
#     },
#     "coordonnees": {
#       "latitude": 48.8566,
#       "longitude": 2.3522
#     },
#     "superficie": {
#       "interieure": 120,  // en mètres carrés
#       "exterieure": 300  // en mètres carrés
#     },
#     "chambres": 3,
#     "salles_de_bain": 2,
#     "amenagements": [
#       "garage",
#       "jardin",
#       "piscine",
#       "terrasse"
#     ],
#     "ensoleillement": "fort",  // Valeurs possibles : faible, moyen, fort
#     "orientation_soleil": "sud",  // Valeurs possibles : nord, sud, est, ouest
#     "date_construction":"2024-06-11T12:00:00Z",
#     "photos": [
#       "url-photo-1.jpg",
#       "url-photo-2.jpg",
#       "url-photo-3.jpg"
#     ],
#     "date_ajout": "2024-07-01T12:00:00Z",
#     "agent": {
#       "nom": "MOHAMED AMEZIANE",
#       "telephone": "0637688422",
#       "email": "med.ameziane@agenceimmobiliere.com"
#     }
#   }
# }

from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime

from models.users import User


class Agent(SQLModel, table=True):
    id: int = Field(primary_key=True, default=None)
    nom: str
    telephone: str
    email: str
    deals: list["Propriete"] = Relationship(back_populates="agent")


# Main Propriete model (real estate listing)
class ProprieteBase(SQLModel):
    titre: str
    description: str
    type: str
    statut: str
    prix: float
    devise: str
    chambres: int
    salles_de_bain: int
    ensoleillement: str
    orientation_soleil: str
    date_construction: datetime
    date_ajout: datetime


class ProprieteUpdate(ProprieteBase):
    pass


class ProprieteCreate(ProprieteBase):
    pass


class ProprietePublic(ProprieteBase):
    id: int
    user: User | None = Relationship(back_populates="propriete")
    agent: Agent = Relationship(back_populates="deals")


class Propriete(ProprieteBase, table=True):
    id: int | None = Field(primary_key=True, default=None)
    user: User | None = Relationship(back_populates="propriete")
    agent: Agent = Relationship(back_populates="deals")
    # Relationships
    adresses: list["Adresse"] = Relationship(back_populates="propriete")
    coordonnees: list["Coordonnees"] = Relationship(back_populates="propriete")
    superficies: list["Superficie"] = Relationship(back_populates="propriete")
    photos: list["Photo"] = Relationship(back_populates="propriete")
    amenagements: list["Amenagement"] = Relationship(back_populates="propriete")
    agent_id: int | None = Field(default=None, foreign_key="agent.id")
    user_id: int | None = Field(default=None, foreign_key="user.id")


# Models for related entities
class Adresse(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    propriete_id: int = Field(foreign_key="propriete.id")
    propriete: Propriete = Relationship(back_populates="adresses")
    rue: str
    ville: str
    region: str
    code_postal: str
    pays: str


class Coordonnees(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    propriete_id: int = Field(foreign_key="propriete.id")
    propriete: Propriete = Relationship(back_populates="coordonnees")
    latitude: float
    longitude: float


class Photo(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    propriete_id: int = Field(foreign_key="propriete.id")
    propriete: Propriete = Relationship(back_populates="photos")
    path: str


class Amenagement(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    propriete_id: int = Field(foreign_key="propriete.id")
    propriete: Propriete = Relationship(back_populates="amenagements")
    type: str


class Superficie(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    propriete_id: int = Field(foreign_key="propriete.id")
    propriete: Propriete = Relationship(back_populates="superficies")
    interieure: float
    exterieure: float
