from playwright.sync_api import Page, expect

from pages.base_page import BasePage


class LoginPage(BasePage):
    def __init__(self, page: Page, base_url: str):
        super().__init__(page, base_url)
        self.username_field = page.get_by_test_id("username")
        self.password_field = page.get_by_test_id("password")
        self.login_button = page.get_by_test_id("login-button")
        self.error_message = page.get_by_test_id("error")

    def open(self):
        self.go()

    def enter_username(self, username: str):
        self.username_field.fill(username)

    def enter_password(self, password: str):
        self.password_field.fill(password)

    def submit(self):
        self.login_button.click()

    def login(self, username: str, password: str):
        self.enter_username(username)
        self.enter_password(password)
        self.submit()

    def expect_success(self):
        expect(self.page).to_have_url(f"{self.base_url}inventory.html")

    def expect_error(self, expected_text: str):
        expect(self.error_message).to_be_visible()
        expect(self.error_message).to_contain_text(expected_text)
