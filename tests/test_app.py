from playwright.sync_api import Page, expect

# Tests for your routes go here

"""
We can render the index page
"""
def test_get_index(page, test_web_address):
    # We load a virtual browser and navigate to the / page
    page.goto(f"http://{test_web_address}/")

    # We look at the <p> tag
    paragraph_tag = page.locator("p")

    # We assert that it has the text "(This is the homepage)"
    expect(paragraph_tag).to_have_text("(This is the homepage)")

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
    page.click("text='Log Out'")
    p_tag = page.locator("p")
    expect(p_tag).to_have_text("(This is the homepage)")


"""
index page loads with all listing showing in a list
"""

def test_listing_on_index_page(db_connection, page, test_web_address):
    db_connection.seed("seeds/makersbnb-red-team.sql")
    page.goto(f"http://{test_web_address}/")

    expect(page.get_by_text("JohnD house")).to_be_visible()
    expect(page.get_by_text("145 JohnD lane, London")).to_be_visible()
    expect(page.get_by_text("Two bedroom flat, next to the sea")).to_be_visible()
    expect(page.get_by_text("£100")).to_be_visible()



# '''
# After logging in, can create a listing
# And listing is added to the databse, and shown on home page listings
# '''
# def test_add_listing(db_connection, page, test_web_address):
#     db_connection.seed("seeds/makersbnb-red-team.sql")
#     page.goto(f"http://{test_web_address}/")
#     page.fill("input[name='email']", "johndoe@example.com")
#     page.fill("input[name='password']", "password123")
#     page.click("input[type='submit']")

