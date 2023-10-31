from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Float, Integer, Text

db = SQLAlchemy()


class Tasks(db.Model):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True)
    price = Column(Float, nullable=False, default=float)
    assignee = Column(Integer, nullable=False)
    description = Column(Text)
