import pytest
import firebase_admin
from firebase_admin import credentials, firestore
from app import create_app
import os
from flask_bcrypt import Bcrypt
import jwt
import datetime

bcrypt = Bcrypt()

def generate_jwt_token(user_id, secret_key):
    payload = {
        'user_id': user_id,
        'exp': datetime.datetime.now() + datetime.timedelta(minutes=30)
    }
    token = jwt.encode(payload, secret_key, algorithm='HS256')
    return token

@pytest.fixture(scope='module')
def app():
    app = create_app()
    app.config.update({
        "TESTING": True,
        "JWT_SECRET_KEY": os.getenv('JWT_SECRET_KEY'),
    })

    if not firebase_admin._apps:
        cred = credentials.Certificate(os.getenv('FIREBASE_TEST_AUTH'))
        firebase_admin.initialize_app(cred)
    app.config['db'] = firestore.client()

    bcrypt.init_app(app)

    yield app

    collections = app.config['db'].collections()
    for collection in collections:
        docs = collection.stream()
        for doc in docs:
            doc.reference.delete()

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def runner(app):
    return app.test_cli_runner()

@pytest.fixture
def bcrypt_instance():
    return bcrypt

@pytest.fixture
def secret_key(app):
    return app.config['JWT_SECRET_KEY']
