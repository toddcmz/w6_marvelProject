import os

class Config():
    SECRET_KEY = os.environ.get('SECRET_KEY') # this is the name of the secret key we assigned in .env
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') # this is the name of the database we assigned in .env