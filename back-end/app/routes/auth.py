import os
from datetime import datetime, timezone, timedelta
from flask import Blueprint, request, jsonify, make_response
from app.utils.auth_utils import get_jwt_identity, jwt_required, generate_verification_token, send_verification_email, verify_verification_token
from app import database
from app.models.models import User, PendingUser
import jwt
from werkzeug.security import check_password_hash


auth_blueprint= Blueprint('auth', __name__)


# homepage route
@auth_blueprint.route('/', methods=['GET'])
def home():
    return '<p>Welcome to the homepage</p>'


# verify email
@auth_blueprint.route('/verify-email', methods=['GET'])
def verify_email():
    try:
        token= request.args.get('token')
        if not token:
            return jsonify({'error':'Missing verification token.'}), 400

        # verify token if token exists
        email= verify_verification_token(token)
        if not email:
            return jsonify({'error': 'Invalid or expired token.'}), 400

        pending_user= PendingUser.query.filter_by(email=email).first()
        if not pending_user:
            return jsonify({'User not found!'}), 404

        # check if the user already exists
        user_exists= User.query.filter_by(email=email).first()
        if user_exists:
            return jsonify({'message':'Email already exists! Please try with a different email.'}), 400

        # collect user data if email is verified. alternatively, use a cache system like redis to store submitted user data until token expires
        # for now we use a pending user database

        # transfer pending user details to new user
        new_user= User(
            fullname= pending_user.fullname,
            email= pending_user.email
        )
        new_user.set_password(pending_user.password)

        # commit new_user to database
        database.session.add(new_user)
        database.session.delete(pending_user)
        database.session.commit()

        # send verified email confirmation

        return jsonify({'message': 'New user created successfully!'}), 201

    except Exception as e:
        database.session.rollback()
        return jsonify({'error': str(e)}), 500


# registration route
@auth_blueprint.route('/signup', methods=['POST'])
def register():
    try:
        # collect pending user data from request
        data = request.get_json()
        email = data.get('email')
        fullname = data.get('fullname')
        password = data.get('password')

        # Check if user already exists
        user_exists = User.query.filter_by(email=email).first()
        if user_exists:
            return jsonify({'message': 'Email already registered! Please log in.'}), 400

        # Check if a pending user exists (in case email was already in pending state)
        pending_user_exists = PendingUser.query.filter_by(email=email).first()
        if pending_user_exists:
            return jsonify({'message': 'Email verification is already pending. Please check your inbox.'}), 400

        # Create a PendingUser entry
        pending_user = PendingUser(
            email=email,
            fullname=fullname,
            password=password  # Don't hash the password yet
        )

        # Generate a verification token for email
        token = generate_verification_token(email)
        pending_user.token= token

        # Add and commit the PendingUser to the database
        database.session.add(pending_user)
        database.session.commit()

        # Send the verification email
        send_verification_email(email, token)

        return jsonify({
            'message': 'Verification email sent. Please check your inbox to verify your email address.',
            'token': token
        }), 200

    except Exception as e:
        # Handle any exceptions and roll back session if needed
        database.session.rollback()
        return jsonify({'error': f'An error occurred during registration: {str(e)}'}), 500



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

        # create response and set the cookie
        response= make_response(jsonify({
            'message':'User logged in successfully!',
            'token': token,
        }))
        response.set_cookie(
            'token',
            token,
            httponly= True,
            secure= True,
            samesite= 'Strict'
        )

        return response, 200

    except Exception as e:
        return jsonify({'error':f'An internal error occurred! {e}'}), 500


# session logout and cookie clearing
@auth_blueprint.route('/logout', methods=['POST'])
def logout():
    response= make_response(jsonify({'message':'You have been logged out!'}))
    response.set_cookie(
        'token',
        '',
        httponly=True,
        expires=0,
        secure=True,
        samesite='Strict'
    )
    return response, 200

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