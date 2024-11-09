import os
from dotenv import load_dotenv


load_dotenv()

class Config:
    SECRET_KEY= os.getenv('SECRET_KEY', 'default_secret_key')
    JWT_SECRET_KEY=os.getenv('JWT_SECRET_KEY', 'jwt_secret_key')
    JWT_TOKEN_LOCATION= os.getenv('JWT_TOKEN_LOCATION', 'headers').split(',')
    JWT_HEADER_NAME='Authorization'
    JWT_HEADER_TYPE='Bearer'
    SQLALCHEMY_DATABASE_URI=os.getenv('DATABASE_URL', 'sqlite:///db.sqlite3')
    SQLALCHEMY_TRACK_MODIFICATIONS= False
    CORS_HEADERS='Content-Type'

class DevelopmentConfig(Config):
    DEBUG= True

class ProductionConfig(Config):
    DEBUG= False