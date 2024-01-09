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
    print(f"Current URL after form submission: {page.url}")
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
    print(f"Current URL after form submission: {page.url}")
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
    page.click("text='Log On'")
    print(f"Current URL after form submission: {page.url}")
    error_message = page.locator(".t-errors")
    expect(error_message).to_have_text("User not found. Please check your email.")