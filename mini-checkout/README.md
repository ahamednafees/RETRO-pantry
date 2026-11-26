# Retro Pantry — Mini Checkout & Browser Test Suite

A responsive, single-page pantry shop and checkout experience. It uses four synthetic products with fixed INR prices and keeps the cart in browser memory. There is no backend, database, payment flow, or external service.

## Features

- Retro Pantry identity with a warm, soft-colour, skeuomorphic interface.
- Four illustrated pantry products with staggered, fluid entrance and hover animations.
- Light/dark theme toggle; the selected theme is remembered in local browser storage.
- Add products, increase/decrease quantities, and remove cart lines using a dedicated, accessible trash button.
- Live line totals, subtotal, fixed ₹40 delivery fee, and order total.
- Constant fictional delivery destination: Retro Pantry, 24 Pantry Lane, Coimbatore, Tamil Nadu 641001.
- Required customer name, empty-basket protection, and clear validation without losing entered data.
- One-time order submission lock and unique order reference.
- Large thank-you confirmation after a successful order.
- Responsive layout, inline SVG icons, and reduced-motion support.

## Fixed catalogue

| Product | Unit price |
|---|---:|
| Sunday Sourdough | ₹180.00 |
| Strawberry Jam | ₹240.00 |
| Olive Grove Oil | ₹420.00 |
| Garden Herb Mix | ₹160.00 |

Delivery fee: **₹40.00** (fixed). The displayed delivery address is fictional sample data and can be changed in `index.html`.

## Run locally

Requires Python 3.9+ (no application dependencies).

```powershell
cd mini-checkout
python -m http.server 8000
```

Open `http://127.0.0.1:8000` in a browser.

## Browser tests

Install the test dependencies once:

```powershell
python -m pip install pytest playwright
python -m playwright install chromium
```

Run the automated browser tests from the `mini-checkout` project root:

```powershell
python -m pytest -v
```

Four tests cover successful checkout, missing-name validation, exact quantity/delivery totals, and the theme toggle/removal control. Each test gets a fresh browser context. Playwright assertions wait for customer-visible states rather than using fixed sleeps.

Run the two repeatable exploratory checks:

```powershell
python tests/manual_checks.py
```

The manual script checks an empty basket and an immediate double-submit, then writes screenshots to `evidence/`.

## Project structure

```text
mini-checkout/
├── index.html
├── styles.css
├── app.js
├── tests/
│   ├── test_checkout.py
│   └── manual_checks.py
├── evidence/
├── README.md
├── TEST_PLAN.md
└── TEST_RESULTS.md
```

## Notes / limitations

Order references are generated in the browser for this prototype only. Refreshing the page resets the cart. No payment or real delivery booking takes place. Google Fonts are optional; local system fonts are fallbacks.
