
import re
from flask import current_app

def is_valid_email(email):
    return re.match(r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$', email) is not None

def check_unique_email(email):
    users_ref = current_app.config['db'].collection('users')
    query = users_ref.where('email', '==', email)
    documents = query.get()
    if not documents:
        return True
    else:
        return False

def check_unique_username(username):
    users_ref = current_app.config['db'].collection('users')
    query = users_ref.where('username', '==', username)
    documents = query.get()
    if not documents:
        return True
    else:
        return False