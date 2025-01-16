from db import db,Exercise, exercise_parser
from app_initialization import socketio, api, app, db
from utils import error_message, response_message
from flask import request

def broadcast_refresh():
    print('Book list broadcast sent.')
    socketio.emit('refresh', get_exercises())  # first parameter is the event name, second parameter is the data to be sent

@socketio.on('connect')
def handle_connect():
    print("Client connected.")
    # broadcast_refresh() # marlaneala de la rares

@socketio.on('disconnect')
def handle_disconnect():
    print("Client disconnected.")

@app.route('/')
def home():
    return response_message("Backend server is running!")


@app.route('/exercises', methods=['GET'])
def get_exercises():
    try:
        exercises = db.session.scalars(db.select(Exercise)).all()
    except Exception as error:
        return error_message(f'Error on retrieving the exercises from the db: {error}')
    return [exercise.serialize() for exercise in exercises]


@app.route('/exercise', methods=['POST'])
def add_exercise():
    try:
        args = exercise_parser.parse_args()
        new_exercise = Exercise(
            name=args['name'],
            description=args.get('description'),
            difficulty=args.get('difficulty'),
            progress=args.get('progress')
        )
        db.session.add(new_exercise)
        db.session.commit()
    except Exception as error:
        return error_message(f'Could not add the exercise to the db: {error}')
    
    broadcast_refresh()
    return response_message(f'Exercise named "{new_exercise.name}" has been added')


@app.route('/exercise/<id>', methods=['PUT'])
def update_exercise(id: int):
    try:
        id = int(id)
    except Exception as error:
        return error_message(f'Id {id} could not be converted to int: {error}')
    
    try:
        exercise = db.session.scalars(db.select(Exercise).where(Exercise.id == id)).first()
        if exercise is None:
            return error_message(f'Exercise with ID {id} not found')
        
        args = exercise_parser.parse_args()
        exercise.name = args['name']
        exercise.description = args.get('description')
        exercise.difficulty = args.get('difficulty')
        db.session.commit()
    except Exception as error:
        return error_message(f'Could not update exercise with id {id}: {error}')
    
    broadcast_refresh()
    return response_message(f'Exercise with ID {id} has been updated')


@app.route('/exercise/<id>', methods=['DELETE'])
def delete_exercise(id: int):
    try:
        id = int(id)
    except Exception as error:
        error_message(f'Id {id} could not be converted to int: {error}')

    try:
        exercise = db.session.scalars(db.select(Exercise).where(Exercise.id == id)).first()
        db.session.delete(exercise)
        db.session.commit()
    except Exception as error:
        return error_message(f'Could not delete exercise with id {id}: {error}')
    
    broadcast_refresh()
    return response_message(f'Exercise with ID {id} has been deleted')


@app.route('/exercise/<int:id>', methods=['GET'])
def get_exercise_by_id(id):
    try:
        id=int(id)
        exercise = db.session.get(Exercise, id)
        if exercise is None:
            return error_message(f'Exercise with id {id} not found'), 404
    except Exception as error:
        return error_message(f'Error retrieving the exercise from the db: {error}')
    return exercise.serialize()


if __name__ == '__main__':
    socketio.run(app, debug=True, allow_unsafe_werkzeug=True, port=5000)