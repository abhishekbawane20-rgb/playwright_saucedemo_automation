import logging

import pytest
from playwright.sync_api import Page, expect

logger = logging.getLogger(__name__)


@pytest.mark.login
@pytest.mark.smoke
def test_login_success(
    page: Page, login_page, saucedemo_credentials
):
    logger.info("Starting valid-user login scenario")
    login_page.open()
    login_page.login(
        saucedemo_credentials.username,
        saucedemo_credentials.password,
    )

    logger.info("Verify login redirects to inventory and products are visible")
    login_page.expect_success()
    expect(page.locator(".inventory_list")).to_be_visible()


@pytest.mark.parametrize(
    ("scenario", "error"),
    [
        pytest.param(
            "empty-username",
            "Username is required",
            id="empty-username",
        ),
        pytest.param(
            "empty-password",
            "Password is required",
            id="empty-password",
        ),
        pytest.param(
            "locked-out-user",
            "Sorry, this user has been locked out.",
            id="locked-out-user",
        ),
    ],
)
@pytest.mark.login
@pytest.mark.regression
def test_login_errors(
    login_page,
    saucedemo_credentials,
    scenario: str,
    error: str,
):
    username = saucedemo_credentials.username
    password = saucedemo_credentials.password
    if scenario == "empty-username":
        username = ""
    elif scenario == "empty-password":
        password = ""
    else:
        username = saucedemo_credentials.locked_out_username

    logger.info("Open login page for negative login scenario")
    login_page.open()
    logger.info("Submit login with username=%r and expected validation=%r", username, error)
    login_page.login(username, password)

    logger.info("Verify expected login error is displayed")
    login_page.expect_error(error)
