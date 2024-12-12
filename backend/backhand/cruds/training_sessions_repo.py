

from .training_session import TrainingSession

class TrainingSessionsRepo:
    def __init__(self, db) -> None:
        self.db=db

    def add_training_session(self, training_session):
        self.db.session.add(training_session)
        self.db.session.commit()
    
    def get_training_session(self, id):
        try:
            training_session = self.db.session.query(TrainingSession).filter(TrainingSession.id == id).one()
            return training_session
        except Exception:
            return None
        
    def training_session_update(self, id, updated_training_session):
        training_session = TrainingSession.query.filter_by(_id=id).first()
        if training_session is not None:
            if updated_training_session.user_id is not None:
                training_session.user_id = updated_training_session.user_id
            if updated_training_session.training_data is not None:
                training_session.training_data = updated_training_session.training_data
            self.db.session.commit()

    def training_session_remove(self, id):
        TrainingSession.query.filter(TrainingSession._id==id).delete()
        self.db.session.commit()
        # training_session = self.get_training_session(id)
        # if training_session is not None:
        #     self.db.session.delete(training_session)
        #     self.db.session.commit()


    def get_all_training_sessions(self, page=1, per_page=10):
        # training_sessions_page = self.db.paginate(self.db.select(TrainingSession).where(TrainingSession.user_type!="admin"))
        training_sessions_page = self.db.paginate(self.db.select(TrainingSession))
        return training_sessions_page
