import logging

import pytest

from pages import ProductsPage

logger = logging.getLogger(__name__)


@pytest.mark.regression
def test_sort_price_low_to_high(products_page: ProductsPage):
    logger.info("Read current product prices and calculate expected ascending order")
    products_before_sort = products_page.products_with_prices()
    expected_order = sorted(products_before_sort, key=lambda product: product[1])

    logger.info("Select price low-to-high and verify displayed product order")
    products_page.sort_by("lohi")

    assert products_page.products_with_prices() == expected_order


@pytest.mark.regression
def test_sort_name_z_to_a(products_page: ProductsPage):
    logger.info("Read current product names and calculate expected descending order")
    expected_order = sorted(products_page.product_names_list(), reverse=True)

    logger.info("Select name Z-to-A and verify displayed product order")
    products_page.sort_by("za")

    assert products_page.product_names_list() == expected_order
