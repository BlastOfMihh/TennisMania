
from .users_repo import UsersRepo
from .user import User

class UsersService:
    def __init__(self, repo: UsersRepo) -> None:
        self.repo = repo

    def user_add(self, username, user_type, is_active, password):
        new_user = User(username, user_type, is_active, password)
        self.xrepo.add(new_user)
    
    def user_remove(self, id):
        self.xrepo.user_remove(id)

    def user_update(self, id, username, user_type, is_active, password):
        updated_user = User(username, user_type, is_active, password)
        self.xrepo.user_update(id, updated_user)

    def user_get(self, id):
        user = self.xrepo.user_get(id)
        return {
            "username": user.username,
            "email": user.email,
        }

    def get_all_users(self, page=1, per_page=10):
        return self.xrepo.get_all_users(page, per_page)