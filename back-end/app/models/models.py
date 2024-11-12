from datetime import datetime, timezone
from app import database
from werkzeug.security import generate_password_hash, check_password_hash


# base model for user models and pending user models inheritances
class BaseUser(database.Model):
    __abstract__= True # prevents this model from becoming a database table

    id= database.Column(database.Integer, primary_key=True)
    fullname= database.Column(database.String(60), unique=True, nullable=False)
    email= database.Column(database.String(120), unique=True, nullable=False)
    created_at= database.Column(database.DateTime, default=datetime.now(timezone.utc))


# pending user model
class PendingUser(BaseUser):
    __tablename__='pending_users'

    # additional fields specific to pending users
    token= database.Column(database.String(500), nullable=False)
    password= database.Column(database.String(20), nullable=False)


# registered user model
class User(BaseUser):
    __tablename__='users'

    # additional fields specific to verified registered users
    is_verified= database.Column(database.Boolean, default=False)
    password_hash= database.Column(database.String(128), nullable=False)

    def set_password(self, password):
        self.password_hash= generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)