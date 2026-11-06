import logging

import pytest
from playwright.sync_api import Page, expect

from pages import CartPage, ProductsPage

logger = logging.getLogger(__name__)


@pytest.mark.regression
def test_remove_cart_item(
    page: Page, products_page: ProductsPage, cart_page: CartPage
):
    logger.info("Add Backpack and Bike Light to the cart")
    products_page.add_backpack()
    products_page.add_bike_light()

    logger.info("Verify badge count and both cart items")
    cart_page.expect_badge("2")
    cart_page.open_cart()
    expect(
        cart_page.cart_items.locator(".inventory_item_name")
    ).to_have_text(["Sauce Labs Backpack", "Sauce Labs Bike Light"])

    logger.info("Remove Backpack and verify remaining cart item and badge")
    page.get_by_test_id("remove-sauce-labs-backpack").click()
    cart_page.expect_badge("1")
    expect(cart_page.cart_items.locator(".inventory_item_name")).to_have_text(
        ["Sauce Labs Bike Light"]
    )
    logger.info("Return to inventory and verify button states and cart badge")
    cart_page.continue_shopping()

    products_page.expect_button_text(
        "add-to-cart-sauce-labs-backpack", "Add to cart"
    )
    products_page.expect_button_text(
        "remove-sauce-labs-bike-light", "Remove"
    )
    cart_page.expect_badge("1")
