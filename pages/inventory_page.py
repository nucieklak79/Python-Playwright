from playwright.sync_api import Page

class InventoryPage:

    def __init__(self, page: Page):
        self.page = page
        self.cart_badge = page.locator(".shopping_cart_link")
        self.cart_link = page.locator("[data-test='shopping-cart-link']")
        self.add_to_cart_template = "[data-test='add-to-cart-{}']"
        self.remove_from_cart_template = "[data-test='remove-{}']"
        self.inventory_item = page.locator(".inventory_item")
        self.sort_dropdown = page.locator(".product_sort_container")
        self.item_prices = page.locator(".inventory_item_price")
        self.inventory_item_names = page.locator(".inventory_item_name")

    def add_product_to_cart(self, product_name_id: str):
        selector = self.add_to_cart_template.format(product_name_id)
        self.page.locator(selector).click()

    def remove_product_from_cart(self, product_name_id: str):
        selector = self.remove_from_cart_template.format(product_name_id)
        self.page.locator(selector).click()

    def go_to_cart(self):
        self.cart_link.click()

    def get_inventory_item_count(self):
        return self.inventory_item

    def sort_products(self, sort_option: str):
        self.sort_dropdown.select_option(sort_option)

    def get_all_names(self):
        return self.inventory_item_names.all_inner_texts()

    def get_all_prices(self):
        return self.item_prices.all_inner_texts()

    
        