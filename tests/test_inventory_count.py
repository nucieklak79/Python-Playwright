from playwright.sync_api import Page, expect

def test_login_page(login_page):
    login_page.navigate()
    login_page.login("standard_user", "secret_sauce")
    expect(login_page.page).to_have_url("https://www.saucedemo.com/inventory.html")

def test_add_product_to_cart(login_page, inventory_page):
    login_page.navigate()
    login_page.login("standard_user", "secret_sauce")
    
    inventory_page.add_product_to_cart("sauce-labs-backpack")
    expect(inventory_page.cart_badge).to_have_text("1")

    inventory_page.remove_product_from_cart("sauce-labs-backpack")
    expect(inventory_page.cart_badge).not_to_have_text("1")

def test_inventory_item_count(login_page, inventory_page):
    login_page.navigate()
    login_page.login("standard_user", "secret_sauce")

    items = inventory_page.get_inventory_item_count()
    expect(items).to_have_count(6)