from app import database
from werkzeug.security import generate_password_hash, check_password_hash


class User(database.Model):
    __tablename__='users'

    id= database.Column(database.Integer, primary_key=True)
    fullname= database.Column(database.String(60), unique=True, nullable=False)
    email= database.Column(database.String(120), unique=True, nullable=False)
    password_hash= database.Column(database.String(128), nullable=False)

    # possible relationships and foreign keys to be defined later

    def set_password(self, password):
        self.password_hash= generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)