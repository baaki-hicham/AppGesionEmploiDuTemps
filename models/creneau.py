from extensions import db
from models.base import BaseModel


class Creneau(BaseModel):
    __tablename__ = 'creneaux'

    jour = db.Column(db.String(50), nullable=False)
    heure_debut = db.Column(db.String(10), nullable=False)
    heure_fin = db.Column(db.String(10), nullable=False)

    seances = db.relationship('Seance', back_populates='creneau', cascade='all, delete-orphan')

    def __repr__(self):
        return f'<Creneau {self.jour} {self.heure_debut}-{self.heure_fin}>'
