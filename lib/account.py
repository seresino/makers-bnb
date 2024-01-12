from peewee import *
from dotenv import load_dotenv
import os

load_dotenv()
db_username = os.getenv('DB_USERNAME')

db = PostgresqlDatabase('makersbnb-red-team', user=db_username, password='', host='localhost')

class Account(Model):
    username = CharField(unique=True)
    first_name = CharField()
    last_name = CharField()
    email = CharField(unique=True)
    password = CharField()
    phone_number = CharField()

    class Meta:
        database = db 