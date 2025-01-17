from db import db, exercise_parser
from app_initialization import socketio, api, app, db
from utils import error_message, response_message
from flask import request, jsonify


import torch
import pickle
import pandas as pd

from notebook import get_model,device

model=get_model().to('cpu')

# def broadcast_refresh():
#     print('Book list broadcast sent.')
#     socketio.emit('refresh', get_exercises())  # first parameter is the event name, second parameter is the data to be sent

# @socketio.on('connect')
# def handle_connect():
#     print("Client connected.")
#     # broadcast_refresh() # marlaneala de la rares

# @socketio.on('disconnect')
# def handle_disconnect():
#     print("Client disconnected.")

# @app.route('/')
# def home():
#     return response_message("Backend server is running!")



@app.route('/predict', methods=['POST'])
def predict():

    print(request.files.getlist('file'))

    # csv_path="./tt csv artificial.CSV"

    df=pd.read_csv(request.files.getlist('file')[0])
    # df=pd.read_csv(csv_path)
    df = df.drop(df.columns[0], axis=1)
    tensor = torch.stack([torch.tensor(df.values)]).to(device)
    
    generation = model.generate(tensor, 10)

    generation_list = generation.tolist()  # Convert tensor to list for JSON serialization
    
    return jsonify({"generation": generation_list})


    

if __name__ == '__main__':
    socketio.run(app, debug=True, allow_unsafe_werkzeug=True, port=5000)