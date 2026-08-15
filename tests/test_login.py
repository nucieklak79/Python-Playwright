import pytest
from playwright.sync_api import expect

@pytest.mark.parametrize("username", ["standard_user", "locked_out_user", "problem_user"])
def test_login_with_multiple_users(login_page, username):

    login_page.navigate()
    login_page.login(username, "secret_sauce")
    
    if username == "locked_out_user":
        expect(login_page.error_message).to_be_visible()
        expect(login_page.error_message).to_contain_text("Epic sadface: Sorry, this user has been locked out.")
    else:
        expect(login_page.page).to_have_url("https://www.saucedemo.com/inventory.html")

def test_login_with_healing(login_page):
    login_page.navigate()

    login_page.page.evaluate('''
    document.querySelector('[data-test="login-button"]').removeAttribute('data-test')
''')
    login_page.login_with_healing("standard_user", "secret_sauce")

    expect(login_page.page).to_have_url("https://www.saucedemo.com/inventory.html")