import os
from dotenv import load_dotenv
import cloudinary

load_dotenv()

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY')
    MONGODB_URI = os.getenv('MONGODB_URI')
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY')
    
cloudinary.config(
    CLOUDINARY_NAME = os.getenv('CLOUDINARY_NAME'),
    CLOUDINARY_API_KEY = os.getenv('CLOUDINARY_API_KEY'),
    CLOUDINARY_API_SECRET = os.getenv('CLOUDINARY_API_SECRET')
)