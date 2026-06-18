from extensions import db
from models.base import BaseModel


class Salle(BaseModel):
    __tablename__ = 'salles'

    nom = db.Column(db.String(100), nullable=False)
    type = db.Column(db.String(100), nullable=False)
    capacite = db.Column(db.Integer, nullable=False)

    seances = db.relationship('Seance', back_populates='salle', cascade='all, delete-orphan')

    def __repr__(self):
        return f'<Salle {self.nom}>'
