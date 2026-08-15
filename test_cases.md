# Test Scenarios & Test Cases — SauceDemo Web Application

**Application Under Test:** https://www.saucedemo.com/
**Related documents:** [`testplan.md`](./testplan.md) for scope and strategy, [`README.md`](./README.md) for how to run the suite.

## Legend

| Field | Values |
|---|---|
| **Priority** | High / Medium / Low |
| **Type** | Positive / Negative / Boundary / Resilience / Data-driven / E2E |
| **Automation status** | ✅ Automated &nbsp;·&nbsp; 🔲 Planned (not yet automated) |

---

## 1. Test Scenarios

High-level testable conditions, grouped by feature. Each scenario is broken down into one or more detailed test cases in §2.

| # | Scenario | Status |
|---|---|---|
| TS-01 | Users with valid, active credentials can log in successfully | ✅ |
| TS-02 | A locked-out user is prevented from logging in and sees a clear error message | ✅ |
| TS-03 | The application is reachable and usable for other standard demo user types | ✅ |
| TS-04 | Login can still complete when a primary UI locator becomes unavailable, via a fallback lookup | ✅ |
| TS-05 | Login is rejected for invalid credentials or empty fields, with an appropriate error message | 🔲 |
| TS-06 | The full product catalog is displayed after login | ✅ |
| TS-07 | Products can be sorted by name (A–Z / Z–A) and price (low–high / high–low), matching the expected order | ✅ |
| TS-08 | A product can be added to the cart and the cart badge updates accordingly | ✅ |
| TS-09 | A product can be removed from the cart and the cart badge updates accordingly | ✅ |
| TS-10 | The cart page correctly lists the item(s) and price(s) that were added from the inventory page | 🔲 |
| TS-11 | A logged-in user can complete the full purchase flow, from adding a product to order confirmation | ✅ |
| TS-12 | The checkout information form validates required fields and blocks progression when data is missing | 🔲 |
| TS-13 | The Checkout Overview screen correctly displays item total, tax, and order total | 🔲 |
| TS-14 | A logged-in user can log out and is returned to the login page | 🔲 |

---

## 2. Detailed Test Cases

### Login

**LOGIN-01 — Successful login with a standard, active user**
- **Priority:** High · **Type:** Positive · **Status:** ✅ Automated
- **Preconditions:** Browser open at the SauceDemo login page
- **Steps:**
  1. Enter username `standard_user`
  2. Enter password `secret_sauce`
  3. Click **Login**
- **Expected result:** User is redirected to `/inventory.html` and the product list is visible
- **Automated as:** `test_login.py::test_login_with_multiple_users[standard_user]`

**LOGIN-02 — Locked-out user is blocked from logging in**
- **Priority:** High · **Type:** Negative · **Status:** ✅ Automated
- **Preconditions:** Browser open at the SauceDemo login page
- **Steps:**
  1. Enter username `locked_out_user`
  2. Enter password `secret_sauce`
  3. Click **Login**
- **Expected result:** User stays on the login page; an error banner is shown containing "Sorry, this user has been locked out."
- **Automated as:** `test_login.py::test_login_with_multiple_users[locked_out_user]`

**LOGIN-03 — Login with a known "problem" demo user still reaches the inventory page**
- **Priority:** Medium · **Type:** Positive / Exploratory · **Status:** ✅ Automated
- **Preconditions:** Browser open at the SauceDemo login page
- **Steps:**
  1. Enter username `problem_user`
  2. Enter password `secret_sauce`
  3. Click **Login**
- **Expected result:** User is redirected to `/inventory.html`
- **Note:** `problem_user` is documented to trigger cosmetic/functional quirks elsewhere in the app (e.g. incorrect product images). This case only checks that login itself succeeds; it is a good candidate for a dedicated follow-up case that asserts the known quirks explicitly.
- **Automated as:** `test_login.py::test_login_with_multiple_users[problem_user]`

**LOGIN-04 — Login recovers when the primary button locator is unavailable (self-healing demo)**
- **Priority:** Medium · **Type:** Resilience / Framework · **Status:** ✅ Automated
- **Preconditions:** Login page loaded; the `data-test` attribute on the login button is removed at runtime to simulate a broken primary locator
- **Steps:**
  1. Fill in valid credentials
  2. Attempt to click the login button via the primary locator (fails by design)
  3. Fallback logic requests an alternative locator and retries the click
- **Expected result:** Login still completes successfully and the user reaches `/inventory.html`, despite the primary locator being unavailable
- **Note:** The fallback locator is currently returned by a mocked/hardcoded stand-in (`MockLLM`), not a live model call — see `README.md` "Known Limitations"
- **Automated as:** `test_login.py::test_login_with_healing`

**LOGIN-05 — Login is rejected with an incorrect password** 🔲 *Planned*
- **Priority:** High · **Type:** Negative
- **Steps:** Enter a valid username with an incorrect password, click **Login**
- **Expected result:** An error message is shown and the user remains on the login page

**LOGIN-06 — Login is rejected when required fields are left empty** 🔲 *Planned*
- **Priority:** Medium · **Type:** Negative / Boundary
- **Steps:** Leave username and/or password blank, click **Login**
- **Expected result:** A field-specific "required" error message is shown; the user remains on the login page

---

### Inventory

**INV-01 — All products are displayed after login**
- **Priority:** Medium · **Type:** Positive · **Status:** ✅ Automated
- **Preconditions:** Logged in as `standard_user`
- **Steps:** Observe the inventory page
- **Expected result:** 6 products are displayed
- **Automated as:** `test_inventory_count.py::test_inventory_item_count`

**INV-02 — Sorting products by name and by price**
- **Priority:** Medium · **Type:** Positive / Data-driven · **Status:** ✅ Automated
- **Preconditions:** Logged in as `standard_user`
- **Steps:** Select each sort option from the dropdown in turn: `Name (A to Z)`, `Name (Z to A)`, `Price (low to high)`, `Price (high to low)`
- **Expected result:** For each option, the displayed order of product names or prices matches the corresponding sorted order of the actual on-page data
- **Automated as:** `test_inventory_sorting.py::test_inventory_sorting[az / za / lohi / hilo]`

---

### Cart

**CART-01 — Add a product to the cart**
- **Priority:** High · **Type:** Positive · **Status:** ✅ Automated
- **Preconditions:** Logged in as `standard_user`
- **Steps:** Click **Add to cart** on "Sauce Labs Backpack"
- **Expected result:** The cart badge displays "1"
- **Automated as:** `test_inventory_count.py::test_add_product_to_cart`

**CART-02 — Remove a product from the cart**
- **Priority:** High · **Type:** Positive · **Status:** ✅ Automated
- **Preconditions:** "Sauce Labs Backpack" already added to the cart (continues from CART-01)
- **Steps:** Click **Remove** on "Sauce Labs Backpack"
- **Expected result:** The cart badge no longer displays "1"
- **Automated as:** `test_inventory_count.py::test_add_product_to_cart`

**CART-03 — Cart page lists the correct product name(s) and price(s)** 🔲 *Planned*
- **Priority:** Medium · **Type:** Positive
- **Steps:** Add a product from the inventory page, open the cart
- **Expected result:** The item shown on the cart page matches the name and price of the product added
- **Note:** `CartPage` currently only exposes the checkout button — it has no locators for cart line items yet

---

### Checkout

**CHK-01 — Complete the full checkout flow (happy path)**
- **Priority:** High · **Type:** Positive / E2E · **Status:** ✅ Automated
- **Preconditions:** Logged in as `standard_user`
- **Steps:**
  1. Add "Sauce Labs Backpack" to the cart
  2. Go to the cart, then proceed to checkout
  3. Fill in first name `Jan`, last name `Kowalski`, postal code `00-001`, click **Continue**
  4. Click **Finish**
- **Expected result:** The order confirmation screen is shown with the text "Thank you for your order!"
- **Automated as:** `test_e2e.py::test_full_checkout_flow`

**CHK-02 — Checkout Step One blocks progression when required fields are empty** 🔲 *Planned*
- **Priority:** High · **Type:** Negative / Validation
- **Steps:** Leave First Name, Last Name, or Postal Code empty and click **Continue**
- **Expected result:** A field-specific "required" error is shown; the user does not advance to the Overview step

**CHK-03 — Checkout Overview correctly displays item total, tax, and order total** 🔲 *Planned*
- **Priority:** High · **Type:** Positive / Calculation
- **Steps:** Proceed to the Overview step with one or more items in the cart
- **Expected result:** The displayed item total equals the sum of the item prices, and the order total equals item total + tax

---

### Session

**SESSION-01 — Logged-in user can log out** 🔲 *Planned*
- **Priority:** Low · **Type:** Positive
- **Steps:** Open the menu and select **Logout**
- **Expected result:** The user is returned to the login page

---

## 3. Coverage Summary

| Module | Automated | Planned |
|---|---|---|
| Login | 4 | 2 |
| Inventory | 2 | 0 |
| Cart | 2 | 1 |
| Checkout | 1 | 2 |
| Session | 0 | 1 |
| **Total** | **9** | **6** |
