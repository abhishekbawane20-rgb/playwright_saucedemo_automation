from playwright.sync_api import Page, expect

from pages.base_page import BasePage


class CheckoutPage(BasePage):
    def __init__(self, page: Page, base_url: str):
        super().__init__(page, base_url)
        self.first_name_field = page.get_by_test_id("firstName")
        self.last_name_field = page.get_by_test_id("lastName")
        self.postal_code_field = page.get_by_test_id("postalCode")
        self.continue_button = page.get_by_test_id("continue")
        self.error_message = page.get_by_test_id("error")
        self.cart_items = page.locator(".cart_item")
        self.overview_item_names = page.locator(
            ".cart_item .inventory_item_name"
        )
        self.item_total = page.locator(".summary_subtotal_label")
        self.tax = page.locator(".summary_tax_label")
        self.total = page.locator(".summary_total_label")
        self.finish_button = page.get_by_test_id("finish")
        self.success_header = page.locator(".complete-header")

    def enter_first_name(self, first_name: str):
        self.first_name_field.fill(first_name)

    def enter_last_name(self, last_name: str):
        self.last_name_field.fill(last_name)

    def enter_postal_code(self, postal_code: str):
        self.postal_code_field.fill(postal_code)

    def continue_checkout(self):
        self.continue_button.click()

    def finish(self):
        self.finish_button.click()

    def enter_info(
        self,
        first_name: str,
        last_name: str,
        postal_code: str,
    ):
        self.enter_first_name(first_name)
        self.enter_last_name(last_name)
        self.enter_postal_code(postal_code)
        self.continue_checkout()

    def expect_step_two(self):
        expect(self.page).to_have_url(f"{self.base_url}checkout-step-two.html")

    def expect_complete(self):
        expect(self.page).to_have_url(f"{self.base_url}checkout-complete.html")

    def expect_error(self, expected_text: str):
        expect(self.error_message).to_be_visible()
        expect(self.error_message).to_contain_text(expected_text)

    def expect_item_count(self, expected_count: int):
        expect(self.cart_items).to_have_count(expected_count)

    def order_summary(self) -> tuple[float, float, float]:
        return (
            self._amount_from_label(self.item_total.inner_text()),
            self._amount_from_label(self.tax.inner_text()),
            self._amount_from_label(self.total.inner_text()),
        )

    def expect_success(self):
        expect(self.success_header).to_be_visible()
        expect(self.success_header).to_have_text("Thank you for your order!")

    def _amount_from_label(self, label: str) -> float:
        return float(label.rsplit("$", 1)[1])
