from lib.listing import Listing

'''
Retrueves all accoutns from seed file
'''
def test_get_all_listings(db_connection):
    db_connection.seed("seeds/makersbnb-red-team.sql")
    listings = Listing.select()
    assert listings[0].id == 1
    assert listings[0].name == 'JohnD house'
    assert listings[0].address == '145 JohnD lane, London'
    assert listings[0].description == 'Two bedroom flat, next to the sea'
    assert listings[0].price == '100'
    assert listings[0].account.id == 1
    


 