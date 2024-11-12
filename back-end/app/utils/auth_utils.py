from functools import wraps                 # for custom decorator wrapping
from flask_mail import Message
from flask import request, jsonify          # for making requests and sending responses
import jwt                                  # for encoding and decoding generated and stored token
import os                                   # for getting environment variables from .env file
from datetime import datetime, timezone, timedelta  # for fetching time/timezone data
from app import mail


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

        except Exception as e:
            print(f'Unexpected error: {e}')
            return jsonify({'error':'An internal server error occurred.'}), 500

        return f(*args, **kwargs)

    return decorated


# get user identity
def get_jwt_identity():
    # access the user_id stored in the request by the decorator
    return getattr(request, 'user_id', None)


# generate verification token for email verification
def generate_verification_token(email):
    if not email:
        raise ValueError('Email cannot be None!')

    payload= {
        'email': email,
        'exp': datetime.now(timezone.utc)+ timedelta(hours=1)
    }
    token= jwt.encode(payload, os.getenv('JWT_SECRET_KEY'), algorithm='HS256')

    return token


# verify if verification token sent to email matches generated token sent to email
def verify_verification_token(token):
    try:
        # decode the JWT encoded token
        payload= jwt.decode(token, os.getenv('JWT_SECRET_KEY'), algorithms=['HS256'])

        # check token expiration first
        exp= payload.get('exp')
        if datetime.now(timezone.utc) > datetime.fromtimestamp(exp, tz=timezone.utc):
            return 'Token expired!'

        # return the email from the token payload if token is still valid
        return payload.get('email')

    except jwt.ExpiredSignatureError as e:
        return e
    except jwt.InvalidTokenError as e:
        return e


# send verification email to user for authentication to account
def send_verification_email(email, token):

    verification_link= f'http://127.0.0.1:5000/verify-email?token={token}'
    msg= Message(
        subject='Email Verification',
        recipients=[email],
        sender= os.getenv('MAIL_USERNAME')
    )
    msg.body= f'Please click on this link to verify your email: {verification_link}'
    try:
        mail.send(msg)
        print('Verification email sent successfully!')
    except Exception as e:
        print(f'Failed to send email: {e}')