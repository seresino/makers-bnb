from peewee import *

db = PostgresqlDatabase('makersbnb-red-team', user='rubyseresin', password='', host='localhost')

class Account(Model):
    username = CharField()
    first_name = CharField()
    last_name = CharField()
    email = CharField()
    password = CharField()
    phone_number = CharField()

    class Meta:
        database = db # This model uses the "people.db" database.