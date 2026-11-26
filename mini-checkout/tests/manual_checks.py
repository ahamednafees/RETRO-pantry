"""Repeatable exploratory checks for empty-cart and rapid double-submit scenarios."""
import os
from pathlib import Path
from playwright.sync_api import sync_playwright, expect

PROJECT = Path(__file__).resolve().parents[1]
CHROMIUM_PATH = os.getenv('CHROMIUM_PATH', '/usr/bin/chromium')
EVIDENCE = PROJECT / 'evidence'
EVIDENCE.mkdir(exist_ok=True)

def load_page(browser):
    page = browser.new_page(viewport={"width": 1365, "height": 1000})
    html = (PROJECT / 'index.html').read_text(encoding='utf-8')
    css = (PROJECT / 'styles.css').read_text(encoding='utf-8')
    js = (PROJECT / 'app.js').read_text(encoding='utf-8')
    html = html.replace('<link rel="stylesheet" href="styles.css" />', f'<style>{css}</style>')
    html = html.replace('<script src="app.js"></script>', f'<script>{js}</script>')
    page.set_content(html, wait_until='domcontentloaded', timeout=10000)
    return page

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True, executable_path=CHROMIUM_PATH if os.path.exists(CHROMIUM_PATH) else None)
    page = load_page(browser)
    page.get_by_label('Who are we packing for?').fill('Test Customer')
    page.get_by_role('button', name='Place my order').click()
    expect(page.get_by_role('alert')).to_contain_text('Your basket is empty')
    expect(page.locator('#confirmation')).to_be_hidden()
    expect(page.get_by_label('Who are we packing for?')).to_have_value('Test Customer')
    page.screenshot(path=str(EVIDENCE / 'empty-cart-validation.png'), full_page=True)
    print('PASS: Empty basket is blocked; name is retained and no confirmation appears.')
    page.close()

    page = load_page(browser)
    page.get_by_role('button', name='Add').first.click()
    page.get_by_label('Who are we packing for?').fill('Double Click Tester')
    button = page.locator('#place-order')
    button.evaluate("el => { el.click(); el.click(); }")
    expect(page.locator('#confirmation')).to_be_visible()
    expect(page.locator('#order-reference')).to_have_text(__import__('re').compile(r'^RP-[A-Z0-9]+-[A-Z0-9]{4}$'))
    expect(page.locator('#confirmation')).to_contain_text('Thank you, Double Click Tester!')
    expect(button).to_be_disabled()
    page.screenshot(path=str(EVIDENCE / 'double-submit-single-confirmation.png'), full_page=True)
    print('PASS: Rapid double submit yields one confirmation/reference; submit button locks.')
    page.close()
    browser.close()
