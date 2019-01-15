"""All served objects needed at beginning of app runtime"""
import os

from flask import Flask

from dotenv import load_dotenv
from playhouse.postgres_ext import PostgresqlExtDatabase

load_dotenv(dotenv_path='./.env')
DATABASE_HOST = os.getenv("DATABASE-HOST")
DATABASE_PORT = os.getenv("DATABASE-PORT")
DATABASE_NAME = os.getenv("DATABASE-NAME")
DATABASE_USER = os.getenv("DATABASE-USER")
DATABASE_PASS = os.getenv("DATABASE-PASS")
CLIENT_ID = os.getenv("CLIENT-ID")
SECRET_KEY = os.getenv("SECRET-KEY")
AUTH0_DOMAIN = os.getenv("AUTH0-DOMAIN")
API_AUDIENCE = os.getenv("API-AUDIENCE")
REDIRECT_URI = os.getenv("REDIRECT-URI")
ACCESS_TOKEN_URL = os.getenv("ACCESS-TOKEN-URL")
AUTHORIZE_URL = os.getenv("AUTHORIZE-URL")
REDIRECT_AUDIENCE = os.getenv("REDIRECT-AUDIENCE")

app = Flask("Vera")
app.config.from_object('config')
db = PostgresqlExtDatabase(
    DATABASE_NAME,
    host=DATABASE_HOST,
    port=DATABASE_PORT,
    user=DATABASE_USER,
    password=DATABASE_PASS)
