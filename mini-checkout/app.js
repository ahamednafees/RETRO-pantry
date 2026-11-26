(() => {
  const products = {
    sourdough: { id: 'sourdough', name: 'Sunday Sourdough', price: 180 },
    jam: { id: 'jam', name: 'Strawberry Jam', price: 240 },
    'olive-oil': { id: 'olive-oil', name: 'Olive Grove Oil', price: 420 },
    herbs: { id: 'herbs', name: 'Garden Herb Mix', price: 160 }
  };
  const DELIVERY_FEE = 40;
  const cart = new Map();
  let orderPlaced = false;
  const money = value => `₹ ${value.toFixed(2)}`;
  const cartElement = document.querySelector('#cart-items');
  const subtotalElement = document.querySelector('#subtotal');
  const totalElement = document.querySelector('#order-total');
  const form = document.querySelector('#checkout-form');
  const nameInput = document.querySelector('#customer-name');
  const validation = document.querySelector('#validation-message');
  const confirmation = document.querySelector('#confirmation');
  const placeButton = document.querySelector('#place-order');
  const themeToggle = document.querySelector('#theme-toggle');
  const root = document.documentElement;

  function applyTheme(theme) {
    root.dataset.theme = theme;
    themeToggle.setAttribute('aria-label', theme === 'dark' ? 'Switch to light mode' : 'Switch to dark mode');
    try { localStorage.setItem('retro-pantry-theme', theme); } catch (_) { /* Storage may be unavailable in private contexts. */ }
  }
  let savedTheme = 'light';
  try { savedTheme = localStorage.getItem('retro-pantry-theme') || 'light'; } catch (_) { /* Keep the light theme. */ }
  applyTheme(savedTheme);
  themeToggle.addEventListener('click', () => applyTheme(root.dataset.theme === 'dark' ? 'light' : 'dark'));

  function render() {
    cartElement.replaceChildren();
    if (cart.size === 0) {
      const empty = document.createElement('div');
      empty.className = 'empty-cart';
      empty.innerHTML = '<span>♡</span><p>Your basket is taking a nap</p><small>Add a pantry favourite to wake it up.</small>';
      cartElement.append(empty);
    } else {
      for (const [id, quantity] of cart) {
        const product = products[id];
        const row = document.createElement('article');
        row.className = 'cart-row';
        row.dataset.product = id;
        row.innerHTML = `<div><h3>${product.name}</h3><span class="unit-price">${money(product.price)} each</span><div class="cart-controls"><div class="quantity-controls"><button type="button" data-action="decrease" aria-label="Decrease ${product.name} quantity"><svg class="icon"><use href="#icon-minus"/></svg></button><output aria-label="${product.name} quantity">${quantity}</output><button type="button" data-action="increase" aria-label="Increase ${product.name} quantity"><svg class="icon"><use href="#icon-plus"/></svg></button></div><button type="button" class="remove-button" data-action="remove" aria-label="Remove ${product.name} from basket" title="Remove ${product.name}"><svg class="icon"><use href="#icon-trash"/></svg></button></div></div><strong class="line-total">${money(product.price * quantity)}</strong>`;
        cartElement.append(row);
      }
    }
    const subtotal = [...cart].reduce((sum, [id, quantity]) => sum + products[id].price * quantity, 0);
    subtotalElement.textContent = money(subtotal);
    document.querySelector('#delivery-fee').textContent = money(DELIVERY_FEE);
    totalElement.textContent = money(subtotal + DELIVERY_FEE);
  }

  document.querySelectorAll('[data-add]').forEach(button => button.addEventListener('click', () => {
    if (orderPlaced) return;
    const id = button.dataset.add;
    cart.set(id, (cart.get(id) || 0) + 1);
    validation.hidden = true;
    render();
  }));

  cartElement.addEventListener('click', event => {
    const button = event.target.closest('button[data-action]');
    if (!button || orderPlaced) return;
    const row = button.closest('[data-product]');
    const id = row.dataset.product;
    const quantity = cart.get(id);
    if (button.dataset.action === 'increase') cart.set(id, quantity + 1);
    if (button.dataset.action === 'decrease') quantity <= 1 ? cart.delete(id) : cart.set(id, quantity - 1);
    if (button.dataset.action === 'remove') cart.delete(id);
    render();
  });

  nameInput.addEventListener('input', () => { if (nameInput.value.trim()) validation.hidden = true; });
  form.addEventListener('submit', event => {
    event.preventDefault();
    if (orderPlaced) return;
    if (cart.size === 0) {
      validation.textContent = 'Your basket is empty. Add a pantry favourite before placing your order.';
      validation.hidden = false;
      return;
    }
    if (!nameInput.value.trim()) {
      validation.textContent = 'Please add your name so we know who to thank.';
      validation.hidden = false;
      nameInput.focus();
      return;
    }
    // Set the lock before any UI update so rapid repeated submits cannot create another order.
    orderPlaced = true;
    const reference = `RP-${Date.now().toString(36).toUpperCase()}-${Math.random().toString(36).slice(2, 6).toUpperCase()}`;
    placeButton.disabled = true;
    placeButton.textContent = 'Order placed ✓';
    validation.hidden = true;
    document.querySelectorAll('.add-button, #cart-items button').forEach(button => button.disabled = true);
    document.querySelector('#confirmation-copy').textContent = `Thank you, ${nameInput.value.trim()}! Your Retro Pantry order is being wrapped with care and will be delivered to 24 Pantry Lane, Coimbatore.`;
    document.querySelector('#order-reference').textContent = reference;
    confirmation.hidden = false;
    confirmation.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
  });
  render();
})();
