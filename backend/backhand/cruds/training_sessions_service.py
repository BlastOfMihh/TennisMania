

from .training_sessions_repo import TrainingSessionsRepo
from .training_session import TrainingSession

class TrainingSessionsService:
    def __init__(self, repo: TrainingSessionsRepo) -> None:
        self.repo = repo

    def training_session_add(self, user_id, training_data):
        new_training_session = TrainingSession(user_id, training_data)
        self.repo.add_training_session(new_training_session)

    def training_session_remove(self, id):
        self.repo.training_session_remove(id)

    def training_session_update(self, id, user_id, training_data):
        updated_training_session = TrainingSession(user_id, training_data)
        self.repo.training_session_update(id, updated_training_session)

    def training_session_get(self, id):
        training_session = self.repo.training_session_get(id)
        return {
            "user_id": training_session.user_id,
            "training_data": training_session.training_data,
        }
    
    def get_all_training_sessions(self, page=1, per_page=10):
        return self.repo.get_all_training_sessions(page, per_page)