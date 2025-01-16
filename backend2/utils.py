import json
from flask import Response
from flask_restful import abort


def response_message(message, status = 200):
    return Response(
        response=json.dumps({
            "message": message
        }),
        status=status,
        mimetype="application/json"
    )

def error_message(message):
    return abort(404, message=message)