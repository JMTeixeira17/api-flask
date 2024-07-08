from datetime import timedelta
from flask import Flask
import firebase_admin
from firebase_admin import credentials, firestore
from dotenv import load_dotenv
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
import os

def create_app():
    app = Flask(__name__)
    bcrypt = Bcrypt(app)
    load_dotenv()
    fsAuth = credentials.Certificate(os.getenv('FIREBASE_AUTH'))
    app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')
    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=2)
    jwt = JWTManager(app)
    firebase_admin.initialize_app(fsAuth)

    db = firestore.client()
    app.config['db'] = db

    from .routes import api
    app.register_blueprint(api, url_prefix='/api')

    return app
