import logging

import pytest
from playwright.sync_api import expect

from pages import CartPage, CheckoutPage, ProductsPage

logger = logging.getLogger(__name__)


@pytest.mark.smoke
def test_checkout_total(
    products_page: ProductsPage,
    cart_page: CartPage,
    checkout_page: CheckoutPage,
):
    logger.info("Add Backpack and Bike Light to the cart")
    products_page.add_backpack()
    products_page.add_bike_light()

    logger.info("Verify cart badge and item contents")
    cart_page.expect_badge("2")
    cart_page.open_cart()
    expect(
        cart_page.cart_items.locator(".inventory_item_name")
    ).to_have_text(["Sauce Labs Backpack", "Sauce Labs Bike Light"])
    logger.info("Proceed to checkout and submit customer information")
    cart_page.checkout()

    checkout_page.enter_info("Alex", "Tester", "12345")
    logger.info("Verify checkout overview contains the expected two items")
    checkout_page.expect_step_two()
    checkout_page.expect_item_count(2)
    expect(checkout_page.overview_item_names).to_have_text(
        ["Sauce Labs Backpack", "Sauce Labs Bike Light"]
    )

    item_total, tax, total = checkout_page.order_summary()
    logger.info(
        "Verify order arithmetic: item total %.2f + tax %.2f = total %.2f",
        item_total,
        tax,
        total,
    )
    assert item_total + tax == pytest.approx(total, abs=0.01)

    logger.info("Finish checkout and verify order confirmation")
    checkout_page.finish()
    checkout_page.expect_complete()
    checkout_page.expect_success()


@pytest.mark.parametrize(
    ("missing_field", "expected_error"),
    [
        pytest.param("first_name", "First Name is required", id="missing-first-name"),
        pytest.param("last_name", "Last Name is required", id="missing-last-name"),
        pytest.param("postal_code", "Postal Code is required", id="missing-postal-code"),
    ],
)
@pytest.mark.regression
def test_checkout_missing_fields(
    products_page: ProductsPage,
    cart_page: CartPage,
    checkout_page: CheckoutPage,
    missing_field: str,
    expected_error: str,
):
    logger.info("Add an item before testing missing %s", missing_field)
    products_page.add_backpack()

    logger.info("Open checkout information form")
    cart_page.open_cart()
    cart_page.checkout()

    if missing_field != "first_name":
        checkout_page.enter_first_name("Alex")
    if missing_field != "last_name":
        checkout_page.enter_last_name("Tester")
    if missing_field != "postal_code":
        checkout_page.enter_postal_code("12345")
    logger.info("Submit form without %s and verify the corresponding error", missing_field)
    checkout_page.continue_checkout()

    checkout_page.expect_error(expected_error)
