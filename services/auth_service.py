import bcrypt
from models.user import User
from extensions import db


class AuthService:
    @staticmethod
    def hash_password(password: str) -> str:
        salt = bcrypt.gensalt()
        return bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')

    @staticmethod
    def check_password(password: str, hashed: str) -> bool:
        return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))

    @staticmethod
    def authenticate(email: str, password: str):
        user = User.query.filter_by(email=email).first()
        if not user:
            return None
        if AuthService.check_password(password, user.password):
            return user
        return None
