import os
from datetime import datetime, timezone, timedelta

from flask import Blueprint, request, jsonify
from app import database
from app.models.models import User
import jwt

auth_blueprint= Blueprint('auth', __name__)

@auth_blueprint.route('/', methods=['GET'])
def home():
    return '<p>Welcome to the homepage</p>'

# registration route
@auth_blueprint.route('/signup', methods=['POST'])
def register():
    try:
        # collect user data from forms
        data= request.get_json()
        fullname= data.get('fullname')
        email= data.get('email')
        password= data.get('password')

        user_exists= User.query.filter_by(email=email).first()
        if user_exists:
            return jsonify({'message':'User email already exists!'}), 400

        new_user= User(fullname=fullname, email=email)
        new_user.set_password(password)

        # commit new_user to database
        database.session.add(new_user)
        database.session.commit()

        return jsonify({'message':'New user created successfully!'}), 201

    except Exception as e:
        print(f'Error: {e}')
        return jsonify({'error':'An internal error occurred.'}), 500


# user login route
@auth_blueprint.route('/login', methods=['POST'])
def login():
    try:
        # collect client-validated user login details, empty fields to be handled client-side
        data= request.get_json()
        email= data.get('email')
        password= data.get('password')

        user= User.query.filter_by(email=email).first()

        if not user:
            return jsonify({'message':'Invalid email!'}), 401
        if password!= user.password_hash:
            return jsonify({'message':'Password incorrect!'}), 401

        # generate token for user login session
        payload= {
            'user_id': user.id,
            'exp': datetime.now(timezone.utc)+ timedelta(hours=3)
        }
        token= jwt.encode(payload, os.getenv('JWT_SECRET_KEY'), algorithm='HS256')

        return jsonify({
                'token':token,
                'message':'User logged in successfully!',
        }), 201

    except Exception as e:
        return jsonify({'error':f'An internal error occurred! {e}'})