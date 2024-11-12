from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from app.config import DevelopmentConfig
from flask_mail import Mail

# define global instances
database= SQLAlchemy()
mail= Mail()

# function to create app
def create_app():
    app= Flask(__name__)

    # app configurations
    app.config.from_object(DevelopmentConfig)

    # initialize global instances
    database.init_app(app)
    CORS(app, resources={r"/*":{"origins": "http://localhost:63343"}}, supports_credentials=True) # CORS configurations to allow use of credentials for using cookies in session
    mail.init_app(app)

    # register blueprints
    from app.routes.auth import auth_blueprint
    app.register_blueprint(auth_blueprint)

    # database initialize
    with app.app_context():
        database.create_all()

    return app