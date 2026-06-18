from extensions import db
from models.base import BaseModel


class Classe(BaseModel):
    __tablename__ = 'classes'

    nom = db.Column(db.String(100), nullable=False)
    niveau = db.Column(db.String(100), nullable=False)
    effectif = db.Column(db.Integer, nullable=False)

    seances = db.relationship('Seance', back_populates='classe', cascade='all, delete-orphan')

    def __repr__(self):
        return f'<Classe {self.nom}>'
