from backhand import db
from sqlalchemy import ForeignKey

from sqlalchemy.orm import Mapped, mapped_column, relationship, DeclarativeBase
from sqlalchemy import String, DateTime, ForeignKey, Boolean, Text


class TrainingSession(db.Model):
    _tablename_='TrainingSessions'

    _id=db.Column(db.Integer, primary_key=True)
    user_id=db.Column(db.Integer, ForeignKey("users._id"), nullable=False)
    training_data=db.Column(db.String, nullable=False)

    def __init__(self, user_id:int, training_data:str):
        self.user_id=user_id
        self.training_data=training_data


    def _repr_(self) -> str:
        return {"id" : self._id, "user_id": self.user_id}