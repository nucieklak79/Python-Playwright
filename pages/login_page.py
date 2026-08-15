from playwright.sync_api import Page, TimeoutError
from utils.ai_helper import MockLLM

class LoginPage:
    def __init__(self, page: Page):
        self.page = page
        self.username_input = page.locator("[data-test='username']")
        self.password_input = page.locator("[data-test='password']")  
        self.login_button_primary = page.locator("[data-test='login-button']")
        self.error_message = page.locator("[data-test='error']")

    def navigate(self):
        self.page.goto("https://www.saucedemo.com/")

    def login(self, username: str, password: str):
        self.username_input.fill(username)
        self.password_input.fill(password)
        self.login_button_primary.click()

    def login_with_healing(self, username: str, password: str):
        self.username_input.fill(username)
        self.password_input.fill(password)
        try:
            self.login_button_primary.click(timeout=3000)
            print("Primary locator used.")

        except TimeoutError:
            print("Primary locator failed. Attempting to heal using LLM")
            current_dom = self.page.content()
            new_locator = MockLLM.guess_new_locator(html_content=current_dom, element_description="login button")

            if new_locator:
                self.page.locator(new_locator).click()
                print(f"Healed locator found: {new_locator}. Attempting to click.")
                
            else:
                raise Exception("Failed to heal locator for login button. No suitable locator found.")