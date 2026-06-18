from extensions import db
from models.base import BaseModel


class Matiere(BaseModel):
    __tablename__ = 'matieres'

    nom = db.Column(db.String(100), nullable=False)
    volume_horaire = db.Column(db.Integer, nullable=False)

    seances = db.relationship('Seance', back_populates='matiere', cascade='all, delete-orphan')

    def __repr__(self):
        return f'<Matiere {self.nom}>'
