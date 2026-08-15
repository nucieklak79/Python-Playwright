import pytest
from playwright.sync_api import Page
from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage

@pytest.mark.parametrize("sort_option", ["az", "za", "lohi", "hilo"])
def test_inventory_sorting(login_page, inventory_page, sort_option: str):
    # Arrange
    login_page.navigate()
    login_page.login("standard_user", "secret_sauce")

    # Act
    inventory_page.sort_products(sort_option)

    if sort_option in ["lohi", "hilo"]:
        prices_text = inventory_page.get_all_prices()
        actual_list = [float(price.replace("$", "")) for price in prices_text]
        expected_list = sorted(actual_list, reverse=(sort_option == "hilo"))

    else:
        actual_list = inventory_page.get_all_names()
        expected_list = sorted(actual_list, reverse=(sort_option == "za"))
        
    # Assert
    assert actual_list == expected_list, f"Sorting by {sort_option} failed. Expected: {expected_list}, but got: {actual_list}"