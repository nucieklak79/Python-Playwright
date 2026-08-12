from playwright.sync_api import Page

class CartPage:
    def __init__(self, page: Page) -> None:
        self.page = page
        self.checkout_button = page.locator("[data-test='checkout']")

    def go_to_checkout(self):
        self.checkout_button.click()       