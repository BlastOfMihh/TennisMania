from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase
from sqlalchemy import String
from flask_restful import reqparse
from flask_sqlalchemy import SQLAlchemy

from collections import OrderedDict


class Base(DeclarativeBase): # NEEDED!
    pass

db = SQLAlchemy(model_class=Base)

exercise_parser = reqparse.RequestParser()
exercise_parser.add_argument('name', type=str, required=True)
exercise_parser.add_argument('difficulty', type=int, required=True)
exercise_parser.add_argument('description', type=str)
exercise_parser.add_argument('progress', type=int)

class Exercise(db.Model):
    __tablename__ = 'books_table'
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    difficulty: Mapped[int] = mapped_column(nullable=True)
    description: Mapped[str] = mapped_column(String(50), nullable=True)
    progress: Mapped[int] = mapped_column(nullable=True)

    def __repr__(self) -> str:
        return f"Book(id={self.id}, name={self.name}, difficulty={self.difficulty}, description={self.description}, progress={self.progress})"

    def serialize(self):
        return OrderedDict({
            "id": self.id,
            "name": self.name,
            "difficulty": self.difficulty,
            "description": self.description,
            "progress": self.progress,
        })