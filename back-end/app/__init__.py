from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from app.config import DevelopmentConfig

# define global instances
database= SQLAlchemy()

# function to create app
def create_app():
    app= Flask(__name__)

    # app configurations
    app.config.from_object(DevelopmentConfig)

    # initialize global instances
    database.init_app(app)
    CORS(app)

    # register blueprints
    from app.routes.auth import auth_blueprint
    app.register_blueprint(auth_blueprint)

    # database initialize
    with app.app_context():
        database.create_all()

    return app