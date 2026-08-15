from playwright.sync_api import Page, expect

def test_full_checkout_flow(login_page, inventory_page, cart_page, checkout_page):
    
    login_page.navigate()
    login_page.login("standard_user", "secret_sauce")

    inventory_page.add_product_to_cart("sauce-labs-backpack")
    inventory_page.go_to_cart()
    
    cart_page.go_to_checkout()
    
    checkout_page.fill_personal_data("Jan", "Kowalski", "00-001")
    checkout_page.finish_checkout()
    
    expect(checkout_page.complete_header).to_have_text("Thank you for your order!")