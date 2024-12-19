from flask_bcrypt import Bcrypt
from flask_cors import CORS
from config import Config
from pymongo import MongoClient
from datetime import datetime, timedelta, timezone
from contextvars import ContextVar
import jwt

bcrypt = Bcrypt()
cors = CORS()

current_user = ContextVar('current_user')
class JWTManager:
    def __init__(self, secret_key, algorithm='HS256'):
        self.secret_key = secret_key
        self.algorithm = algorithm
    def create_token(self, data, expires_in=3600):
        payload = data.copy()
        payload["exp"] = datetime.now(timezone.utc) + timedelta(seconds=expires_in)
        return jwt.encode(payload, self.secret_key, algorithm=self.algorithm)
    def decode_token(self, token):
        try:
            decoded=jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
            return decoded
        except jwt.ExpiredSignatureError:
            raise ValueError("Expired token")
        except jwt.InvalidTokenError:
            raise ValueError("Invalid token")

jwt_manager = JWTManager(secret_key=Config.JWT_SECRET_KEY)

mongo_client = MongoClient(Config.MONGODB_URI)
mongo_db = mongo_client['google_classroom'] 
profile = mongo_db['profile']
student = mongo_db['student']
instructor = mongo_db['instructor']
course = mongo_db['course']