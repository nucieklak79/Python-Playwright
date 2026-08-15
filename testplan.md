# Test Plan — SauceDemo Web Application

| | |
|---|---|
| **Project** | SauceDemo Test Automation (Portfolio Project) |
| **Application Under Test (AUT)** | https://www.saucedemo.com/ |
| **Document version** | 1.0 |
| **Author** | Norbert |
| **Date** | 2026-08-15 |

## 1. Introduction

This document defines the test plan for the automated UI regression suite covering the core shopping flow of the SauceDemo web application (a public demo e-commerce site maintained by Sauce Labs for training and framework-practice purposes). It was written as part of a portfolio project intended to demonstrate the ability to plan, scope, and structure functional test coverage — not only to write automation code.

## 2. Objectives

- Verify that the core purchasing flow (login → browse/sort inventory → cart → checkout) behaves correctly for the application's standard demo user types.
- Provide a maintainable, Page-Object-Model-based automated regression suite that can be extended over time.
- Give reviewers a clear, honest picture of current test coverage and known gaps, with traceability between documented test cases and the automated tests that implement them (see `test_cases.md`).

## 3. Scope

### 3.1 In Scope (Features Under Test)

- **Login** — successful login for multiple demo user types, locked-out user rejection, resilience of the login flow when a primary UI locator is unavailable
- **Inventory / product listing** — product count on page load, sorting by name and by price
- **Cart** — adding a product, removing a product, cart badge count
- **Checkout** — Step One ("Your Information") happy path and order confirmation

### 3.2 Out of Scope (current version)

| Item | Reason |
|---|---|
| Checkout Step Two — Overview (item total / tax / total price validation) | Page object does not yet expose Overview-step locators; logged as a planned gap, not silently skipped |
| Negative/validation testing of the checkout form (empty required fields) | Not yet automated — documented as planned test cases in `test_cases.md` |
| Logout flow | Not yet automated |
| Cross-browser / cross-device execution matrix | Suite currently targets Chromium only; no `pytest.ini`/browser matrix configured yet |
| Performance, accessibility, security, and API-level testing | Outside the scope of this UI-focused project |
| Visual regression testing | Not attempted in this version |
| CI/CD pipeline execution | Tests are currently run locally only |

## 4. Test Approach / Strategy

- **Type of testing:** Functional UI regression testing (black-box)
- **Design pattern:** Page Object Model (POM) — locators and page interactions are encapsulated in `pages/`, kept independent of test logic in `tests/`
- **Data-driven testing:** `pytest.mark.parametrize` is used for multi-user login checks and multi-option sorting checks, rather than duplicating near-identical test functions
- **Assertion style:** Playwright's web-first `expect()` API (auto-retrying, auto-waiting), avoiding hardcoded sleeps for UI state changes
- **Test levels covered:** UI-level system/functional testing only — no unit or API-level tests are included in this suite
- **Test types included:** Positive testing (happy paths), a limited set of negative testing (locked-out user), and one resilience/robustness scenario (self-healing locator fallback)
- **Test documentation:** every automated test is traceable to a documented test case in `test_cases.md`; planned-but-not-yet-automated cases are documented there as well, rather than only existing as code

## 5. Test Environment

| Item | Details |
|---|---|
| Application under test | https://www.saucedemo.com/ (public Sauce Labs demo application) |
| Browser | Chromium (Playwright's default; no browser matrix configured yet) |
| Operating system | Cross-platform (Windows / macOS / Linux) |
| Language / runtime | Python 3.10+ |
| Test framework | pytest 8.0.0 |
| Automation library | Playwright 1.41.0, via `pytest-playwright` 0.4.0 |
| Test data | Built-in SauceDemo demo accounts (e.g. `standard_user` / `secret_sauce`) |

## 6. Entry Criteria

- Python, pytest, and Playwright (with browser binaries via `playwright install`) are installed
- The application under test (saucedemo.com) is reachable and stable
- Test code and page objects have been reviewed
- Demo account credentials are available and unchanged

## 7. Exit Criteria

- All planned automated test cases for the current scope have been executed
- No open Critical/High-severity defects block the core flows (login, add-to-cart, checkout happy path)
- Test results have been reviewed and summarized
- Known gaps (§3.2) are explicitly documented rather than silently omitted

## 8. Suspension & Resumption Criteria

- **Suspend testing if:** the AUT is unreachable, login is fully broken (which blocks every downstream flow), or the local environment cannot install the required dependencies.
- **Resume when:** the blocking issue is resolved and a smoke check (`test_login_with_multiple_users[standard_user]`) passes again.

## 9. Test Deliverables

- Automated test scripts (`tests/`) and page objects (`pages/`)
- This test plan (`testplan.md`)
- Test scenarios and detailed test cases (`test_cases.md`)
- Test execution output (currently console/pytest output; no persisted report format is integrated yet — see §11)

## 10. Roles & Responsibilities

| Role | Responsibility | Owner |
|---|---|---|
| Test Automation Engineer | Test design, scripting, execution, and reporting | Norbert |

## 11. Risks & Mitigations

| Risk | Likelihood | Impact | Mitigation |
|---|---|---|---|
| Public demo site changes its markup/attributes over time | Low | Medium | `data-test` attributes are used as the primary locator strategy, which is more stable than CSS classes or XPath; a self-healing fallback concept is prototyped in `utils/ai_helper.py` |
| No CI pipeline yet — the suite only runs locally, so regressions between runs can go unnoticed | Medium | Medium | Planned improvement: add a GitHub Actions workflow (see README "Next Steps") |
| No persisted test report — results are only visible in the console | Medium | Low | Planned improvement: integrate `pytest-html` or Allure reporting |
| Checkout Overview (pricing/tax) step is untested | Medium | Medium | Logged explicitly as an out-of-scope gap (§3.2) and prioritized as the next automation task, rather than being silently uncovered |
| Base URL and credentials are hardcoded rather than externalized | Low | Low | Planned improvement: move to environment variables / a config fixture |

## 12. Tools Summary

- **Language:** Python
- **Test runner:** pytest
- **Browser automation:** Playwright
- **Version control:** Git (recommended for the full project; not bundled in this export)
- **IDE:** VS Code / PyCharm (either works)

## 13. Milestones

*Informal, self-paced schedule for a portfolio project.*

| Milestone | Status |
|---|---|
| POM structure and shared fixtures | Done |
| Login coverage (multi-user, locked-out, self-healing demo) | Done |
| Inventory coverage (item count, sorting) | Done |
| Cart coverage (add/remove) | Done |
| Checkout happy-path E2E coverage | Done |
| Checkout Overview (price/tax) coverage | Planned |
| Negative/boundary checkout and login tests | Planned |
| CI integration (GitHub Actions) | Planned |
| Test reporting (Allure / pytest-html) | Planned |
