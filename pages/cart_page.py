from playwright.sync_api import Page, expect


class CartPage:
    def __init__(self, page: Page):
        self.cart_link = page.locator(".shopping_cart_link")
        self.cart_badge = page.locator(".shopping_cart_badge")
        self.cart_items = page.locator(".cart_item")
        self.checkout_button = page.get_by_test_id("checkout")
        self.continue_shopping_button = page.get_by_test_id("continue-shopping")

    def open_cart(self):
        self.cart_link.click()

    def checkout(self):
        self.checkout_button.click()

    def continue_shopping(self):
        self.continue_shopping_button.click()

    def expect_badge(self, count: str):
        expect(self.cart_badge).to_be_visible()
        expect(self.cart_badge).to_have_text(count)
