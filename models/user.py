from extensions import db
from models.base import BaseModel


class User(BaseModel):
    __tablename__ = 'users'

    nom = db.Column(db.String(100), nullable=False)
    prenom = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(50), nullable=False, default='Admin')

    def __repr__(self):
        return f'<User {self.email}>'
