from dotenv import load_dotenv
import os
SECRET_KEY = os.urandom(32)
# Grabs the folder where the script runs.
basedir = os.path.abspath(os.path.dirname(__file__))

# Enable debug mode.
DEBUG = True

# Connect to the database
db_password = os.getenv("db_password")

# TODO IMPLEMENT DATABASE URL
SQLALCHEMY_DATABASE_URI = f'postgresql://postgres:{db_password}@localhost:5432/fyyurdb'
SQLALCHEMY_TRACK_MODIFICATIONS=False
