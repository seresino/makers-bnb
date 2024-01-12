import os
from peewee import *
from lib.account import Account
from dotenv import load_dotenv

load_dotenv()
db_username = os.getenv('DB_USERNAME')

db = PostgresqlDatabase('makersbnb-red-team', user=db_username, password='', host='localhost')

class Listing(Model):
    name = CharField()
    address = CharField()
    description = CharField()
    price = CharField()
    account = ForeignKeyField(Account, backref='listings')
    image_filename = CharField() 
    

    class Meta:
        database = db # This model uses the "people.db" database.