from flask_bcrypt import Bcrypt
from flask_cors import CORS
from config import Config
from pymongo import MongoClient

bcrypt = Bcrypt()
cors = CORS()

mongo_client = MongoClient(Config.MONGODB_URI)
mongo_db = mongo_client['google_classroom'] 