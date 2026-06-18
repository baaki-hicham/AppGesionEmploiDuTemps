from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect

# Extension instances shared across the application
# This avoids multiple SQLAlchemy instances when app.py is executed as __main__
db = SQLAlchemy()
csrf = CSRFProtect()
