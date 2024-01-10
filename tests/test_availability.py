from lib.availability import Availability
from datetime import date, datetime

"""
Retrieves data from availability table
"""

def test_returns_data(db_connection):
    db_connection.seed("seeds/makersbnb-red-team.sql")
    availability = Availability.select()

    assert availability[0].id == 1
    assert availability[0].listing_id.id == 1
    assert str(availability[0].start_date) == '2024-02-01'
    assert str(availability[0].end_date) == '2024-02-10'
    assert availability[0].available == True


    assert availability[3].id == 4
    assert availability[3].listing_id.id == 3
    assert str(availability[3].start_date) == '2024-02-03'
    assert str(availability[3].end_date) == '2024-02-05'
    assert availability[3].available == True



