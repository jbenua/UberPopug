from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Float, Integer, String

db = SQLAlchemy()


class Popugs(db.Model):
    __tablename__ = "popugs"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    beak_size = Column(Integer, unique=True)
    account = Column(Float, nullable=False, default=float)
