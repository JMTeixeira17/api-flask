import jwt
import datetime

def generate_jwt_token(user_id, secret_key):
    payload = {
        'user_id': user_id,
        'exp': datetime.datetime.now() + datetime.timedelta(minutes=30)
    }
    token = jwt.encode(payload, secret_key, algorithm='HS256')
    return token
