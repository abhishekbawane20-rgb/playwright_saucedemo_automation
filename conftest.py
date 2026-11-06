import os
from dataclasses import dataclass
from typing import Callable, Generator
from urllib.parse import urljoin

import pytest
from playwright.sync_api import Browser, BrowserContext, Page, expect

from pages import CartPage, CheckoutPage, LoginPage, ProductsPage


@dataclass(frozen=True)
class SauceDemoCredentials:
    username: str
    password: str
    locked_out_username: str


def _configured_value(
    config: pytest.Config,
    option: str,
    environment_variable: str,
    setting: str,
) -> str | None:
    return (
        config.getoption(option)
        or os.getenv(environment_variable)
        or config.getini(setting)
    )


def pytest_addoption(parser: pytest.Parser) -> None:
    for name, description, default in (
        ("browser", "Default browser engine.", "chromium"),
        ("saucedemo_username", "Default SauceDemo user name.", "standard_user"),
        ("saucedemo_password", "Default SauceDemo password.", "secret_sauce"),
        ("locked_out_username", "Locked-out SauceDemo user name.", "locked_out_user"),
    ):
        parser.addini(name, description, default=default)

    parser.addoption("--saucedemo-username", default=None, help="SauceDemo user name.")
    parser.addoption("--saucedemo-password", default=None, help="SauceDemo password.")
    parser.addoption(
        "--locked-out-username",
        default=None,
        help="Locked-out SauceDemo user name.",
    )


def pytest_configure(config: pytest.Config) -> None:
    if not config.getoption("--browser"):
        browser = os.getenv("PLAYWRIGHT_BROWSER") or config.getini("browser")
        if browser not in {"chromium", "firefox", "webkit"}:
            raise pytest.UsageError("Browser must be chromium, firefox, or webkit.")
        config.option.browser = [browser]

    if not config.getoption("base_url") and os.getenv("PYTEST_BASE_URL"):
        config.option.base_url = os.getenv("PYTEST_BASE_URL")


@pytest.fixture(scope="session")
def configure_test_id_attribute(playwright) -> None:
    playwright.selectors.set_test_id_attribute("data-test")


@pytest.fixture(scope="session")
def saucedemo_credentials(pytestconfig: pytest.Config) -> SauceDemoCredentials:
    username = _configured_value(
        pytestconfig,
        "--saucedemo-username",
        "SAUCEDEMO_USERNAME",
        "saucedemo_username",
    )
    password = _configured_value(
        pytestconfig,
        "--saucedemo-password",
        "SAUCEDEMO_PASSWORD",
        "saucedemo_password",
    )
    locked_out_username = _configured_value(
        pytestconfig,
        "--locked-out-username",
        "SAUCEDEMO_LOCKED_OUT_USERNAME",
        "locked_out_username",
    )
    if not username or not password or not locked_out_username:
        raise pytest.UsageError(
            "Set SauceDemo credentials in pytest.ini, environment variables, "
            "or CLI options."
        )
    return SauceDemoCredentials(username, password, locked_out_username)


@pytest.fixture(scope="session")
def app_base_url(pytestconfig: pytest.Config) -> str:
    base_url = (
        pytestconfig.getoption("base_url")
        or os.getenv("PYTEST_BASE_URL")
        or pytestconfig.getini("base_url")
    )
    if not base_url:
        raise pytest.UsageError(
            "Set the app URL with --base-url, PYTEST_BASE_URL, or pytest.ini."
        )
    return base_url


@pytest.fixture(scope="session")
def authenticated_storage_state(
    browser: Browser,
    app_base_url: str,
    saucedemo_credentials: SauceDemoCredentials,
    configure_test_id_attribute: None,
) -> dict[str, object]:
    context = browser.new_context(base_url=app_base_url)
    try:
        page = context.new_page()
        login_page = LoginPage(page, app_base_url)
        login_page.open()
        login_page.login(
            saucedemo_credentials.username,
            saucedemo_credentials.password,
        )
        expect(page).to_have_url(
            urljoin(app_base_url.rstrip("/") + "/", "inventory.html")
        )
        return context.storage_state()
    finally:
        context.close()


@pytest.fixture
def context(
    request: pytest.FixtureRequest,
    new_context: Callable[..., BrowserContext],
) -> Generator[BrowserContext, None, None]:
    options: dict[str, object] = {}
    if not request.node.get_closest_marker("login"):
        options["storage_state"] = request.getfixturevalue(
            "authenticated_storage_state"
        )
    browser_context = new_context(**options)
    yield browser_context
    browser_context.close()


@pytest.fixture
def page(
    request: pytest.FixtureRequest,
    context: BrowserContext,
    app_base_url: str,
    configure_test_id_attribute: None,
) -> Generator[Page, None, None]:
    page = context.new_page()
    if not request.node.get_closest_marker("login"):
        page.goto(urljoin(app_base_url.rstrip("/") + "/", "inventory.html"))
    yield page


@pytest.fixture
def login_page(page: Page, app_base_url: str) -> LoginPage:
    return LoginPage(page, app_base_url)


@pytest.fixture
def products_page(page: Page) -> ProductsPage:
    return ProductsPage(page)


@pytest.fixture
def cart_page(page: Page) -> CartPage:
    return CartPage(page)


@pytest.fixture
def checkout_page(page: Page, app_base_url: str) -> CheckoutPage:
    return CheckoutPage(page, app_base_url)
