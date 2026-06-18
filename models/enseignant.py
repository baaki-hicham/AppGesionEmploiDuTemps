from extensions import db
from models.base import BaseModel


class Enseignant(BaseModel):
    __tablename__ = 'enseignants'

    nom = db.Column(db.String(100), nullable=False)
    prenom = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    telephone = db.Column(db.String(50), nullable=True)
    specialite = db.Column(db.String(100), nullable=True)
    disponibilite = db.Column(db.String(255), nullable=True)

    seances = db.relationship('Seance', back_populates='enseignant', cascade='all, delete-orphan')

    def __repr__(self):
        return f'<Enseignant {self.nom} {self.prenom}>'
