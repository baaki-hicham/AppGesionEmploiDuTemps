from extensions import db
from models.base import BaseModel


class Seance(BaseModel):
    __tablename__ = 'seances'

    classe_id = db.Column(db.Integer, db.ForeignKey('classes.id'), nullable=False)
    enseignant_id = db.Column(db.Integer, db.ForeignKey('enseignants.id'), nullable=False)
    matiere_id = db.Column(db.Integer, db.ForeignKey('matieres.id'), nullable=False)
    salle_id = db.Column(db.Integer, db.ForeignKey('salles.id'), nullable=False)
    creneau_id = db.Column(db.Integer, db.ForeignKey('creneaux.id'), nullable=False)

    classe = db.relationship('Classe', back_populates='seances')
    enseignant = db.relationship('Enseignant', back_populates='seances')
    matiere = db.relationship('Matiere', back_populates='seances')
    salle = db.relationship('Salle', back_populates='seances')
    creneau = db.relationship('Creneau', back_populates='seances')

    def __repr__(self):
        return f'<Seance classe={self.classe_id} enseignant={self.enseignant_id} creneau={self.creneau_id}>'
