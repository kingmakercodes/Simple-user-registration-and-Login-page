import os
from datetime import datetime, timezone, timedelta
from flask import Blueprint, request, jsonify
from app.utils.auth_utils import get_jwt_identity, jwt_required
from app import database
from app.models.models import User
import jwt
from werkzeug.security import check_password_hash


auth_blueprint= Blueprint('auth', __name__)


# homepage route
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

        # session rollback to avoid database locking issues
        database.session.rollback()

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

        # fetch specific attributes to reduce query time
        user = User.query.with_entities(User.id, User.fullname, User.email, User.password_hash).filter_by(email=email).first()

        if not user:
            return jsonify({'message':'User does not exist!'}), 404
        else:
            valid_pass= check_password_hash(user.password_hash, password)
            if not valid_pass:
                return jsonify({'error':'Invalid password!'}), 401

        # generate token for user login session if user exists
        payload= {
            'sub':user.id,
            'user_id': user.id,
            'exp': datetime.now(timezone.utc)+ timedelta(hours=3)
        }
        token= jwt.encode(payload, os.getenv('JWT_SECRET_KEY'), algorithm='HS256')

        return jsonify({
                'token':token,
                'message':'User logged in successfully!',
        }), 200

    except Exception as e:
        return jsonify({'error':f'An internal error occurred! {e}'}), 500


# user profile route
@auth_blueprint.route('/profile', methods=['GET'])
@jwt_required
def fetch_user_profile():
    user_id= get_jwt_identity()
    user= User.query.get(user_id)

    if not user:
        return jsonify({'error':'User not found!'}), 404

    user_details= {
        'id': user.id,
        'fullname': user.fullname,
        'email': user.email
    }
    return jsonify(user_details), 200