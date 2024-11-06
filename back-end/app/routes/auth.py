from flask import Blueprint, request, jsonify
from app import database
from app.models.models import User

auth_blueprint= Blueprint('auth', __name__)

@auth_blueprint.route('/', methods=['GET'])
def home():
    return '<p>Welcome to the homepage</p>'

# registration route
@auth_blueprint.route('/signup', methods=['POST'])
def register():
    try:
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