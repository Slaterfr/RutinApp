import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    DATABASE_URI = os.getenv('DATABASE_URI')
    SECRET_KEY = os.getenv('SECRET_KEY')
    TOKEN_ALGORITH = os.getenv('JWT_ALGORITHM')
    JWT_EXPIRATION = os.getenv('JWT_EXPIRATION')
    GROQ_KEY = os.getenv('GROQ_API_KEY')