from lib.account import Account

'''
Retrieves all accounts from seed file
'''
def test_get_all_accounts(db_connection):
    db_connection.seed("seeds/makersbnb-red-team.sql")
    accounts = Account.select()
    assert accounts[0].id == 1
    assert accounts[0].username == 'JohnD'
    assert accounts[0].first_name == 'John'
    assert accounts[0].last_name == 'Doe'
    assert accounts[0].email == 'johndoe@example.com'
    assert accounts[0].password == 'password123'
    assert accounts[0].phone_number == '07973661188'