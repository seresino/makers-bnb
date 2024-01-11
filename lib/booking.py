import os
from peewee import *
from lib.listing import Listing
from lib.account import Account
from dotenv import load_dotenv

load_dotenv()
db_username = os.getenv('DB_USERNAME')

db = PostgresqlDatabase('makersbnb-red-team', user=db_username, password='', host='localhost')

class Booking(Model):
    listing_id = ForeignKeyField(Listing, backref='listing')
    account_id = ForeignKeyField(Account, backref='account')
    start_date = DateField()
    end_date = DateField()
    status = CharField()

    class Meta:
        database = db 