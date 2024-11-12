import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY= os.getenv('SECRET_KEY', 'default_secret_key')

    # JWT configuration keys
    JWT_SECRET_KEY=os.getenv('JWT_SECRET_KEY', 'jwt_secret_key')
    JWT_TOKEN_LOCATION= os.getenv('JWT_TOKEN_LOCATION', 'headers').split(',')
    JWT_HEADER_NAME='Authorization'
    JWT_HEADER_TYPE='Bearer'

    # SQLALCHEMY database configuration keys
    SQLALCHEMY_DATABASE_URI=os.getenv('DATABASE_URL', 'sqlite:///db.sqlite3')
    SQLALCHEMY_TRACK_MODIFICATIONS= False

    # CORS configuration key
    CORS_HEADERS='Content-Type'

    # FLASK-MAIL configuration keys
    MAIL_SERVER= os.getenv('MAIL_SERVER')
    MAIL_PORT= os.getenv('MAIL_PORT')
    MAIL_USE_TLS= os.getenv('MAIL_USE_TLS')== 'True'
    MAIL_USE_SSL= os.getenv('MAIL_USE_SSL')== 'True'
    MAIL_USERNAME= os.getenv('MAIL_USERNAME')
    MAIL_PASSWORD= os.getenv('MAIL_PASSWORD')
    MAIL_DEFAULT_SENDER= os.getenv('MAIL_DEFAULT_SENDER')

class DevelopmentConfig(Config):
    DEBUG= True

class ProductionConfig(Config):
    DEBUG= False