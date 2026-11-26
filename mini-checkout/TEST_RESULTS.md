# Retro Pantry — Test Results

## Execution environment

Python 3.13.5, pytest 9.0.2, Playwright Python, Chromium 144.0.7559.96 (headless). The tests load local HTML, CSS, and JavaScript into isolated Chromium pages; no backend, payment provider, or remote service is used.

## Automated checks

| ID | Check | Result | Evidence |
|---|---|---|---|
| A1 | Successful checkout, personalized thank-you, and reference | **PASS** | `evidence/success-confirmation.png` |
| A2 | Missing name blocks checkout and preserves basket | **PASS** | Automated assertion: validation visible, Strawberry Jam and ₹280.00 order total remain, confirmation hidden |
| A3 | Quantity and exact subtotal/delivery/order total | **PASS** | Two sourdoughs: line/subtotal ₹360.00 + delivery ₹40.00 = total ₹400.00 |
| A4 | Dark theme toggle and dedicated remove control | **PASS** | Theme attribute changes to dark; remove empties basket and totals recalculate |

Automated run: **4 passed in 5.78s**.

## Manual / exploratory checks

| ID | Check | Result | Evidence |
|---|---|---|---|
| M1 | Empty basket blocks checkout and retains entered name | **PASS** | `evidence/empty-cart-validation.png` |
| M2 | Rapid double-submit creates one confirmation/reference | **PASS** | `evidence/double-submit-single-confirmation.png` |
| V1 | Dark-mode appearance | **CAPTURED** | `evidence/dark-mode.png` |
| V2 | Narrow mobile layout | **CAPTURED** | `evidence/mobile-layout.png` |

Manual script output:

```text
PASS: Empty basket is blocked; name is retained and no confirmation appears.
PASS: Rapid double submit yields one confirmation/reference; submit button locks.
```

## Defects

No application defects were observed in the updated automated and manual checks. The test results above refer to the Retro Pantry version in this submission.
