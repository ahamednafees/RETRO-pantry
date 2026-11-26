# Retro Pantry — Test Plan

## Scope and priorities

| Priority | Risk | Coverage | Expected result |
|---|---|---|---|
| P0 | Incorrect order amount | Add two Sunday Sourdough loaves; inspect line, subtotal, delivery, total | Line/subtotal ₹360.00 + fixed ₹40.00 delivery = ₹400.00 |
| P0 | Invalid order accepted | Submit with basket empty or name blank | Clear validation; no confirmation; entered name and cart remain intact |
| P0 | Duplicate order from rapid double-click | Trigger two submit events immediately | One confirmation/reference; submit action locks |
| P0 | Wrong delivery fee or destination | Inspect basket delivery card and totals | Fixed sample address is visible; delivery remains ₹40.00 |
| P1 | Quantity/remove controls corrupt basket | Increase, decrease, remove a line | Counts and all totals recalculate; empty state returns |
| P1 | Theme switch breaks visibility | Switch light → dark → light | Theme changes without losing cart state |
| P1 | Product cards feel static or obscure controls | Load page, inspect staggered cards and hover/add controls | Cards animate smoothly; controls remain readable and operable |
| P1 | Confirmation is ambiguous | Place a valid order | Large thank-you message and one reference are visible |

## Automated browser cases

1. **Successful checkout** — clean page; add Sunday Sourdough; enter a name; place order; assert large thank-you heading, personalized message, reference format, and disabled submit button.
2. **Missing required field** — clean page; add Strawberry Jam; leave name blank; place order; assert validation, retained cart/total, and no confirmation.
3. **Exact quantity and delivery total** — clean page; add two Sunday Sourdough loaves; assert quantity 2, line/subtotal ₹360.00, delivery ₹40.00, and order total ₹400.00.
4. **Theme and remove control** — switch to dark mode; add a product; use the dedicated remove icon; assert empty state and recalculated totals.

Each automated test gets a new browser context and clean page. Assertions use Playwright's auto-waiting expectations.

## Exploratory/manual scenarios

- **Empty basket:** leave the basket empty, enter a name, and place the order. Expected: blocked, explanatory message, no confirmation, name retained.
- **Rapid double-click:** add an item, enter a name, and trigger two submit events immediately. Expected: only one confirmation and one reference; button becomes disabled.

Run `python tests/manual_checks.py` to repeat these checks and save evidence screenshots. Also inspect the theme toggle, product-card motion, responsive layout, and remove button manually at desktop and mobile widths.

## Defect reporting

Report only observed defects. Include browser/version, reproducible steps, expected result, actual result, and a screenshot or trace. A test setup/selector problem is not an application defect.
