from playwright.sync_api import Page, expect

# Tests for your routes go here

"""
We can render the index page
"""
def test_get_index(page, test_web_address):
    # We load a virtual browser and navigate to the /index page
    page.goto(f"http://{test_web_address}/")

    # We look at the <p> tag
    strong_tag = page.locator("p")

    # We assert that it has the text "(This is the homepage)"
    expect(strong_tag).to_have_text("(This is the homepage)")

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

