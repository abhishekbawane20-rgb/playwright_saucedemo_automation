from playwright.sync_api import Page, expect


class ProductsPage:
    def __init__(self, page: Page):
        self.page = page
        self.products = page.locator(".inventory_item")
        self.product_names = page.locator(".inventory_item_name")
        self.product_prices = page.locator(".inventory_item_price")
        self.sort_dropdown = page.get_by_test_id("product-sort-container")

    def add_backpack(self):
        self.page.get_by_test_id("add-to-cart-sauce-labs-backpack").click()

    def add_bike_light(self):
        self.page.get_by_test_id("add-to-cart-sauce-labs-bike-light").click()

    def sort_by(self, option: str):
        self.sort_dropdown.select_option(option)

    def product_names_list(self) -> list[str]:
        expect(self.products.first).to_be_visible()
        return self.product_names.all_text_contents()

    def products_with_prices(self) -> list[tuple[str, float]]:
        names = self.product_names_list()
        prices = [
            float(price.removeprefix("$"))
            for price in self.product_prices.all_text_contents()
        ]
        return list(zip(names, prices))

    def expect_button_text(self, test_id: str, expected_text: str):
        expect(self.page.get_by_test_id(test_id)).to_have_text(expected_text)
