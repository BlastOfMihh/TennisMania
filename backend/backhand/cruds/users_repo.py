
from .user import User

class UsersRepo:
    def __init__(self, db) -> None:
        self.db=db

    def add_user(self, user):
        self.db.session.add(user)
        self.db.session.commit()

    def get_user(self, id):
        try:
            user = self.db.session.query(User).filter(User.id == id).one()
            return user
        except Exception:
            return None

    def user_update(self, id, updated_user):
        user = User.query.filter_by(_id=id).first()
        if user is not None:
            if updated_user.username is not None:
                user.username = updated_user.username
            if updated_user.password is not None:
                user.password = updated_user.password
            if updated_user.is_active is not None:
                user.is_active = updated_user.is_active
            if updated_user.user_type is not None:
                user.user_type = updated_user.user_type
            self.db.session.commit()

    def user_remove(self, id):
        User.query.filter(User._id==id).delete()
        self.db.session.commit()
        # user = self.get_user(id)
        # if user is not None:
        #     self.db.session.delete(user)
        #     self.db.session.commit()

    def get_all_users(self, page=1, per_page=10):
        # users_page = self.db.paginate(self.db.select(User).where(User.user_type!="admin"))
        users_page = self.db.paginate(self.db.select(User))
        return users_page

    