import os
from peewee import *
from lib.listing import Listing
from dotenv import load_dotenv

load_dotenv()
db_username = os.getenv('DB_USERNAME')

db = PostgresqlDatabase('makersbnb-red-team', user=db_username, password='', host='localhost')

class Availability(Model):
    listing_id = ForeignKeyField(Listing, backref='listing')
    start_date = DateField()
    end_date = DateField()
    available = BooleanField()
    requested = BooleanField()

    class Meta:
        database = db 