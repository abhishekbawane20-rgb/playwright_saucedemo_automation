# Playwright SauceDemo UI Tests

Python UI automation for SauceDemo using Playwright, pytest, and the Page Object Model (POM).

## Coverage

| Area | Scenarios |
|---|---|
| Login | Valid login, locked-out user, and empty username/password validation |
| Products | Verify displayed order for price ascending and name descending |
| Cart | Remove a product and verify inventory controls and badge |
| Checkout | Two-item purchase and totals; missing first name, last name, and postal code |

The suite collects 11 cases, including parameterized validation scenarios.

## Project layout

```text
pages/                 Page objects and shared page behavior
tests/                 UI scenarios
conftest.py            Configuration and pytest page-object fixtures
pytest.ini             Defaults and test markers
requirements.txt       Pinned Python dependencies
run_tests.sh           Parallel test runner and report generation
azure-pipelines.yml    Azure Pipelines CI definition
sample-reports/        Example JUnit XML and HTML reports
reports/               Generated reports (git-ignored)
test-results/          Failure-only Playwright artifacts (git-ignored)
```

## Setup

Requires Python 3.10+ and pip.

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
playwright install chromium
```

On Windows, activate the virtual environment with `.venv\Scripts\activate`.

## Run tests

Run the complete suite in parallel and generate JUnit XML and a self-contained HTML report:

```bash
bash run_tests.sh
```

Reports are written to `reports/`. Playwright traces, screenshots, and videos are retained only for failures under `test-results/`.

To refresh the example reports:

```bash
REPORTS_DIR=sample-reports bash run_tests.sh
```

Other useful commands:

```bash
pytest tests/ --headed
pytest -m smoke
pytest -m regression
```

## Configuration

Defaults are in `pytest.ini`. The base URL, browser, and SauceDemo credentials can be overridden using pytest CLI options or environment variables:

- Base URL: `--base-url` or `PYTEST_BASE_URL`
- Browser: `--browser` or `PLAYWRIGHT_BROWSER`
- Credentials: `--saucedemo-username`, `--saucedemo-password`, and `--locked-out-username`, or `SAUCEDEMO_USERNAME`, `SAUCEDEMO_PASSWORD`, and `SAUCEDEMO_LOCKED_OUT_USERNAME`

CLI values take precedence over environment variables, which take precedence over `pytest.ini`. Use the public SauceDemo test credentials by default; avoid putting private credentials in project files.

The authenticated storage state is reused by tests that do not carry the `login` marker. With pytest-xdist, the session-scoped fixture runs once per worker. Login tests use a fresh unauthenticated context.

## Page Object Model

Page objects encapsulate locators and user actions, while tests describe the scenarios and assertions. They are provided as pytest fixtures in `conftest.py`. For example:

```python
from playwright.sync_api import Page
from pages.base_page import BasePage


class LoginPage(BasePage):
    def __init__(self, page: Page, base_url: str):
        super().__init__(page, base_url)
        self.username_field = page.get_by_test_id("username")
        self.password_field = page.get_by_test_id("password")
        self.login_button = page.get_by_test_id("login-button")

    def login(self, username: str, password: str):
        self.username_field.fill(username)
        self.password_field.fill(password)
        self.login_button.click()
```

## Azure Pipelines

The pipeline runs for pushes and pull requests. It selects Python 3.13, installs the pinned dependencies and Chromium, runs `run_tests.sh`, publishes JUnit results with `PublishTestResults@2`, and uploads the HTML reports and failure artifacts as pipeline artifacts. Publication steps run even if tests fail.

The `poolName` parameter selects a self-hosted pool. Leave it empty to use the Microsoft-hosted image selected by `vmImage` (default: `ubuntu-latest`). A self-hosted agent must provide a compatible Linux environment and Python 3.13.
