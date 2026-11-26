import os
import re
from pathlib import Path
import pytest
from playwright.sync_api import sync_playwright, expect

PROJECT = Path(__file__).resolve().parents[1]
CHROMIUM_PATH = os.getenv('CHROMIUM_PATH', '/usr/bin/chromium')

@pytest.fixture(scope='session')
def browser():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True, executable_path=CHROMIUM_PATH if os.path.exists(CHROMIUM_PATH) else None)
        yield browser
        browser.close()

@pytest.fixture
def page(browser):
    context = browser.new_context(viewport={"width": 1365, "height": 1000}, color_scheme="light")
    page = context.new_page()
    html = (PROJECT / 'index.html').read_text(encoding='utf-8')
    css = (PROJECT / 'styles.css').read_text(encoding='utf-8')
    js = (PROJECT / 'app.js').read_text(encoding='utf-8')
    html = html.replace('<link rel="stylesheet" href="styles.css" />', f'<style>{css}</style>')
    html = html.replace('<script src="app.js"></script>', f'<script>{js}</script>')
    page.set_content(html, wait_until='domcontentloaded', timeout=10000)
    yield page
    context.close()

def test_successful_checkout_shows_confirmation_and_reference(page):
    page.get_by_role('button', name='Add').first.click()
    page.get_by_label('Who are we packing for?').fill('Ahamed')
    page.get_by_role('button', name=re.compile('Place my order')).click()
    expect(page.get_by_role('heading', name='Thank you for shopping with us!')).to_be_visible()
    expect(page.get_by_text(re.compile(r'Thank you, Ahamed! Your Retro Pantry order is being wrapped'))).to_be_visible()
    reference = page.locator('#order-reference')
    expect(reference).to_have_text(re.compile(r'^RP-[A-Z0-9]+-[A-Z0-9]{4}$'))
    expect(page.locator('#place-order')).to_be_disabled()
    page.screenshot(path=str(PROJECT / 'evidence' / 'success-confirmation.png'), full_page=True)

def test_missing_name_blocks_checkout_and_preserves_cart(page):
    page.get_by_role('button', name='Add').nth(1).click()
    page.get_by_role('button', name=re.compile('Place my order')).click()
    expect(page.get_by_role('alert')).to_have_text('Please add your name so we know who to thank.')
    expect(page.locator('#cart-items').get_by_role('heading', name='Strawberry Jam')).to_be_visible()
    expect(page.locator('#order-total')).to_have_text('₹ 280.00')
    expect(page.locator('#confirmation')).to_be_hidden()

def test_quantity_change_updates_exact_line_and_order_totals(page):
    page.get_by_role('button', name='Add').first.click()
    page.get_by_role('button', name='Add').first.click()
    row = page.locator('[data-product="sourdough"]')
    expect(row.locator('output')).to_have_text('2')
    expect(row.locator('.line-total')).to_have_text('₹ 360.00')
    expect(page.locator('#subtotal')).to_have_text('₹ 360.00')
    expect(page.locator('#delivery-fee')).to_have_text('₹ 40.00')
    expect(page.locator('#order-total')).to_have_text('₹ 400.00')

def test_theme_toggle_and_remove_button_work(page):
    theme = page.locator('html')
    toggle = page.get_by_role('button', name='Switch to dark mode')
    toggle.click()
    expect(theme).to_have_attribute('data-theme', 'dark')
    expect(page.get_by_role('button', name='Switch to light mode')).to_be_visible()
    page.get_by_role('button', name='Add').first.click()
    page.get_by_role('button', name='Remove Sunday Sourdough from basket').click()
    expect(page.locator('#cart-items').get_by_text('Your basket is taking a nap')).to_be_visible()
    expect(page.locator('#subtotal')).to_have_text('₹ 0.00')
    expect(page.locator('#order-total')).to_have_text('₹ 40.00')
