# models/__init__.py
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# Import model(s) to bind them to the db instance
from .ski_resort import SkiResort
