from functools import wraps                 # for custom decorator wrapping
from flask import request, jsonify          # for making requests and sending responses
import jwt                                  # for encoding and decoding generated and stored token
import os                                   # for getting environment variables from .env file
from datetime import datetime, timezone     # for fetching time/timezone data


def jwt_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token= None

        # check if token is in the Authorization header
        if 'Authorization' in request.headers:
            token= request.headers['Authorization'].split(' ')[1] # extract token from Bearer <token>

        # if no token is found, return an error
        if not token:
            return jsonify({'message':'Token is missing!'}), 401

        try:
            # decode the token if it exists
            payload= jwt.decode(token, os.getenv('JWT_SECRET_KEY'), algorithms=['HS256'])

            # store user information from token for access within the route
            request.user_id= payload['user_id']

        # handle possible error exceptions
        except jwt.ExpiredSignatureError:
            return jsonify({'message': 'Token has expired!'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'message':'Invalid token!'}), 401

        return f(*args, **kwargs)

    return decorated


def get_jwt_identity():
    # access the user_id stored in the request by the decorator
    return getattr(request, 'user_id', None)