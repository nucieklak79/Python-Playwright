# SauceDemo Test Automation Framework (Python + Playwright)

A UI test automation project for [saucedemo.com](https://www.saucedemo.com/), built with **Python**, **pytest**, and **Playwright**, following the **Page Object Model (POM)** design pattern.

This is a portfolio project created to demonstrate practical test automation skills for a Junior Software Tester role: framework structure, maintainable locators, data-driven testing, and test documentation.

## Tech Stack

| Category | Tool |
|---|---|
| Language | Python 3.10+ |
| Test framework | pytest |
| Browser automation | Playwright (via `pytest-playwright`) |
| Design pattern | Page Object Model (POM) |
| Fixtures | Centralized in `conftest.py` |

## Key Features

- **Page Object Model** — locators and page actions live in `pages/`, fully separated from test logic in `tests/`.
- **Reusable pytest fixtures** for each page object, defined once in `conftest.py`.
- **Data-driven tests** using `pytest.mark.parametrize` — e.g. one test function covers three login user types, another covers four sorting options, instead of duplicating near-identical tests.
- **Resilient locators** — most elements are located via the app's dedicated `data-test` attributes rather than fragile CSS classes or XPath.
- **Web-first assertions** — Playwright's auto-waiting `expect()` API is used throughout instead of manual/hardcoded waits.
- **Self-healing locator concept** (`utils/ai_helper.py`) — a small proof-of-concept showing how a broken primary locator could trigger a fallback lookup for an alternative one, so a UI test can recover instead of failing outright.
  > **Note for reviewers:** in this version, `MockLLM` is a hardcoded stand-in that returns a fixed selector for one known case — it does not call a real language model. It demonstrates the *pattern* (detect failure → request a fallback locator → retry) rather than a production-ready implementation.

## Project Structure

```
.
├── conftest.py                    # Shared pytest fixtures (page objects)
├── requirements.txt                # Python dependencies
├── pages/                          # Page Object Model
│   ├── login_page.py
│   ├── inventory_page.py
│   ├── cart_page.py
│   └── checkout_page.py
├── tests/                          # Test suite
│   ├── test_login.py
│   ├── test_inventory_count.py
│   ├── test_inventory_sorting.py
│   └── test_e2e.py
├── utils/
│   └── ai_helper.py                # Self-healing locator proof-of-concept
├── testplan.md                     # Test plan (scope, strategy, environment, risks)
└── test_cases.md                   # Test scenarios and detailed test cases
```

## Getting Started

### Prerequisites

- Python 3.10 or newer
- pip

### Installation

```bash
git clone <repo-url>
cd <project-folder>

python -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate

pip install -r requirements.txt
playwright install            # downloads the browser binaries Playwright needs
```

### Running the tests

```bash
pytest                        # run the full suite
pytest tests/test_login.py    # run a single file
pytest -k "sorting"           # run tests matching a keyword
pytest -v                     # verbose output
pytest --headed                # run with a visible browser window
pytest --headed --browser firefox   # run against a different browser
```

## Scope of Testing

**Covered by automated tests:**
- Login — valid login for multiple user types, locked-out user error handling, resilience to a broken primary locator
- Inventory — product count on load, sorting by name (A–Z / Z–A) and price (low–high / high–low)
- Cart — adding and removing a product, cart badge count
- Checkout — full happy-path flow from cart to order confirmation

**Not yet covered** (see `testplan.md` §3.2 and `test_cases.md` for the full list and rationale):
- Checkout Overview step (item total / tax / total price validation)
- Checkout form validation for missing required fields
- Logout flow
- Cross-browser execution matrix

## Test Documentation

- [`testplan.md`](./testplan.md) — formal test plan: objectives, scope, strategy, environment, entry/exit criteria, risks
- [`test_cases.md`](./test_cases.md) — test scenarios and detailed test cases, cross-referenced to the automated tests that implement them

## Known Limitations

- The self-healing locator (`MockLLM`) is simulated, not connected to a live LLM API, in this version.
- The base URL and demo credentials are currently hardcoded in the page objects/tests rather than externalized via environment variables or a config file.
- No CI pipeline or persisted test report (e.g. HTML/Allure) is included yet — results are currently read from the console.

## Possible Next Steps

- Extend `CheckoutPage` to cover the Overview step and add price/tax verification
- Add negative and boundary tests (empty checkout fields, empty cart, invalid login)
- Replace `MockLLM` with a real LLM API call behind the same interface
- Externalize configuration (base URL, credentials) via environment variables
- Add a GitHub Actions workflow to run the suite on every push
- Integrate Allure (or `pytest-html`) for persisted, shareable test reports

## Author

Norbert Ucieklak
n.ucieklak@gmail.com

https://www.linkedin.com/in/norbert-ucieklak-274b12343/
