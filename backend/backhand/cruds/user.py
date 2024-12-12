from backhand import db
from flask_login import UserMixin

class User(db.Model, UserMixin):
    __tablename__='users'
    _id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.Text, unique=True, nullable=False)
    user_type = db.Column(db.Text, nullable=False)
    is_active = db.Column(db.Boolean, default=True)
    password = db.Column(db.Text, nullable=False)

    def __init__(self, username, user_type, is_active, password):
        self.username=username
        self.user_type=user_type
        self.is_active=is_active
        self.password=password

    def __repr__(self):
        return f'<User {self.username}>'

    def to_dict(self):
        return {"id" : self._id, "username": self.username, "user_type":self.user_type, "is_active":self.is_active}