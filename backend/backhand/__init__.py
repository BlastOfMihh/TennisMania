from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from backhand.cruds.users_controller import register_routes
from backhand.cruds.training_sessions_controller import training_sessions_routes
from backhand.cruds import bp 


from flask import jsonify, session, request, redirect, url_for
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity, get_jwt
from flask_bcrypt import bcrypt

from flask_socketio import SocketIO


db=SQLAlchemy() if 'db' not in locals() else db
jwt=JWTManager() if 'jwt' not in locals() else jwt
socketio=SocketIO(cors_allowed_origins="*") if 'socketio' not in locals() else socketio

from .cruds.user import User

def create_app():
    app=Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///./mydb.db'

    # for the JWT thing
    app.config['SECRET_KEY'] = 'stronger_than_water'
    app.config["JWT_SECRET_KEY"] = 'balanced_as_fire'
    app.config['JWT_TOKEN_LOCATION'] = ['headers']
    CORS(app)

    db.init_app(app)
    from backhand.cruds.users_repo import UsersRepo
    from backhand.cruds.training_sessions_repo import TrainingSessionsRepo
    from backhand.cruds.users_service import UsersService
    from backhand.cruds.training_sessions_service import TrainingSessionsService
    # app.register_blueprint(bp)
    jwt.init_app(app=app)
    socketio.init_app(app=app)

    users_repo=UsersRepo(db)
    training_sessions_repo=TrainingSessionsRepo(db)
    users_service=UsersService(users_repo)
    training_sessions_service=TrainingSessionsService(training_sessions_repo)
    register_routes(app,socketio, users_service)
    training_sessions_routes(app,socketio, training_sessions_service)

    migrate=Migrate(app, db)

    
    @app.route('/login', methods=['POST'])
    def login():
        data = request.get_json()
        username = data['username']
        password = data['password']
        print('Received data:', username , password)

        user = User.query.filter_by(username=username).first()

        if user : #and bcrypt.check_password_hash(user.password, password):
            access_token = create_access_token(
                identity=
                {
                    "id":user._id,
                    "user_type":user.user_type
                })
            return {
                'message': 'Login Success', 
                'access_token': access_token,
                'username':user.username,
                'user_type':user.user_type
            }
        else:
            return {'message': 'Login Failed'}, 401
    
    @app.route('/register', methods=['POST'])
    def register():
        data = request.get_json()
        username = data['username']
        user_type = data['user_type']
        password = data['password']
        print('Received data:', username , password)
        new_user = User(username=username, user_type=user_type, password=password, is_active=True)
        db.session.add(new_user)
        db.session.commit()
        # if user and bcrypt.check_password_hash(user.password, password):
        #     access_token = create_access_token(identity=user.id)
        #     return {'message': 'Login Success', 'access_token': access_token}
        # else:
        #     return {'message': 'Login Failed'}, 401
        return 'registerd'
        return {'registerd'},401

    return app, socketio, db