from playwright.sync_api import Page, expect

# Tests for your routes go here

"""
We can render the index page
"""
def test_get_index(page, test_web_address):
    # We load a virtual browser and navigate to the / page
    page.goto(f"http://{test_web_address}/")

    # We look at the <p> tag
    heading = page.locator("h1")

    # We assert that it has the text "(This is the homepage)"
    expect(heading).to_have_text("Welcome to MakersBnb!")

"""
We can render the signup page
"""
def test_get_signup(page, test_web_address):
    page.goto(f"http://{test_web_address}/signup")
    page.wait_for_selector("h1")
    strong_tag = page.locator("h1")
    expect(strong_tag).to_have_text("Sign Up")

"""
After entering information, the signup page redirects to the / page for the user
"""
def test_post__valid_signup(page, test_web_address, db_connection):
    db_connection.seed("seeds/makersbnb-red-team.sql")
    page.goto(f"http://{test_web_address}/signup")
    page.fill("input[name='username']", "newuser")
    page.fill("input[name='firstname']", "new")
    page.fill("input[name='lastname']", "user")
    page.fill("input[name='email']", "new@email.com")
    page.fill("input[name='phone']", "0207777777")
    page.fill("input[name='password']", "123")
    page.click("input[type='submit']")
    print(page.content())
    heading_tag = page.locator("h1")
    expect(heading_tag).to_have_text("Welcome to MakersBnb!")
    username = page.locator(".user")
    expect(username).to_have_text("Hello, newuser!")

"""
We can render the login page
"""
def test_get_login(page, test_web_address):
    page.goto(f"http://{test_web_address}/login")
    strong_tag = page.locator("h1")
    expect(strong_tag).to_have_text("Log In")


"""
After entering a valid email and password, the login page redirects to the / page greeting the user
"""
def test_post__valid_login(page, test_web_address, db_connection):
    db_connection.seed("seeds/makersbnb-red-team.sql")
    page.goto(f"http://{test_web_address}/login")
    page.fill("input[name='email']", "johndoe@example.com")
    page.fill("input[name='password']", "password123")
    page.click("input[type='submit']")
    heading_tag = page.locator("h1")
    expect(heading_tag).to_have_text("Welcome to MakersBnb!")
    username = page.locator(".user")
    expect(username).to_have_text("Hello, JohnD!")


"""
After entering invalid password, the login page shows the corresponding error
"""
def test_post_invalid_password(page, test_web_address, db_connection):
    db_connection.seed("seeds/makersbnb-red-team.sql")
    page.goto(f"http://{test_web_address}/login")
    page.fill("input[name='email']", "johndoe@example.com")
    page.fill("input[name='password']", "wrongpassword")
    page.click("input[type='submit']")
    error_message = page.locator(".t-errors")
    expect(error_message).to_have_text("Incorrect password. Please try again.")


"""
After entering invalid email, the login page shows the corresponding error
"""
def test_post_invalid_email(page, test_web_address, db_connection):
    db_connection.seed("seeds/makersbnb-red-team.sql")
    page.goto(f"http://{test_web_address}/login")
    page.fill("input[name='email']", "wrongemail@example.com")
    page.fill("input[name='password']", "password123")
    page.click("input[type='submit']")
    error_message = page.locator(".t-errors")
    expect(error_message).to_have_text("User not found. Please check your email.")

"""
Once logged in, pressing log out takes you back to the / page without a greeting
"""
def test_log_out(page, test_web_address, db_connection):
    db_connection.seed("seeds/makersbnb-red-team.sql")
    page.goto(f"http://{test_web_address}/login")
    page.fill("input[name='email']", "johndoe@example.com")
    page.fill("input[name='password']", "password123")
    page.click("input[type='submit']")
    page.click('a[href="/logout"]')
    heading = page.locator("h1")
    expect(heading).to_have_text("Welcome to MakersBnb!")


"""
index page loads with all listing showing in a list
"""

def test_listing_on_index_page(db_connection, page, test_web_address):
    db_connection.seed("seeds/makersbnb-red-team.sql")
    page.goto(f"http://{test_web_address}/")

    expect(page.get_by_text("JohnD house")).to_be_visible()
    expect(page.get_by_text("£100")).to_be_visible()


'''
After logging in, can create a listing
And listing is added to the databse, and shown on home page listings
'''
def test_add_listing(db_connection, page, test_web_address):
    db_connection.seed("seeds/makersbnb-red-team.sql")
    page.goto(f"http://{test_web_address}/login")
    page.fill("input[name='email']", "kat@example.com")
    page.fill("input[name='password']", "password1236")
    page.click("input[type='submit']")
    page.click('a[href="/add-space"]')
    page.fill("input[name='name']", "KatB")
    page.fill("input[name='address']", "Test address")
    page.fill("input[name='description']", "Test description")
    page.fill("input[name='price']", "10")
    page.click("input[type='submit']")
    h1_tag = page.locator("h1")
    expect(h1_tag).to_have_text("KatB")


"""
When we click on a listing, it takes us through to relevant booking page
"""
def test_get_listing(page, test_web_address, db_connection):
    db_connection.seed("seeds/makersbnb-red-team.sql")
    page.goto(f"http://{test_web_address}/")
    page.click("text='JohnD house'")
    address = page.locator(".address")
    expect(address).to_have_text("Address: 145 JohnD lane, London")

'''
When we signup with correct username, first and last names, phone and password, but wrong email
error message display
'''
def test_sign_up_with_correct_details(page, test_web_address, db_connection):
    db_connection.seed("seeds/makersbnb-red-team.sql")
    page.goto(f"http://{test_web_address}/signup")
    page.fill("input[name='username']", "TestUser")
    page.fill("input[name='firstname']", "Name")
    page.fill("input[name='lastname']", "Surname")
    page.fill("input[name='email']", "test")
    page.fill("input[name='phone']", "7999999999")
    page.fill("input[name='password']", "password1")
    page.click("input[type='submit']")
    heading_tag = page.locator("h1")
    error_message = page.locator(".t-errors")
    expect(error_message).to_have_text("Invalid email address.")

