# Problem Statement
We need to replace the instant one-click order mechanism with a fully-fledged eCommerce checkout page (`checkout.html`). This page must feature a modern, premium design mirroring the core brand aesthetic, allow users to review their cart items ("cart history"), see their total bill, provide shipping details, and select between multiple payment methods (COD, Credit Card, UPI, etc.) before officially placing the order with the backend.

# Steps
1. **Create `checkout.html` UI**
   - Implement a two-column grid layout (Left: Shipping & Payment, Right: Order Summary).
   - *Expected Output*: A visually stunning, highly-responsive checkout page using existing CSS globals (vibrant dark mode, modern typography).

2. **Develop Checkout Flow Logic (`checkout.js` or inline script)**
   - Extract cart items from `localStorage` (`Cart.getItems()`) and render them in the Order Summary.
   - Calculate Subtotal, mock Shipping fees, and Final Total.
   - Implement basic UI interactivity for Payment Methods (e.g., showing card input fields when "Credit/Debit Card" is selected, hiding when "COD" is selected).
   - *Expected Output*: The checkout page correctly displays the user's cart contents and interactive payment method selector.

3. **Wire Submit Button to Backend API**
   - Intercept the "Place Order" form submission.
   - Package the selected shipping/payment data and cart items into the payload.
   - Fire a `POST` request to `http://localhost:8000/orders/` using the JWT auth token.
   - *Expected Output*: An explicitly logged order in the backend database.

4. **Update `app.js` and other links**
   - Change the `Checkout` button inside the Cart Flyout to `window.location.href = 'checkout.html'` instead of immediately firing the API request.
   - *Expected Output*: All generic checkout paths correctly route to the new page.

# Verification Method
- Ensure clicking the cart's "Checkout" natively redirects the user.
- Visually verify that the new checkout UI matches the rich aesthetic of `login.html` and `index.html`.
- Try pacing an order via COD and via Credit Card; both must successfully hit the connected PostgreSQL DB backend without breaking.

# Risks & Assumptions
- *Assumption*: The `POST /orders/` endpoint already accepts our mock `shipping_address` payload format. We will dynamically populate it with real inputs from the form.
- *Risk*: The cart flyout logic heavily relies on `Cart.getItems()`. We assume `Cart` can be properly read via the existing `product-data.js` and `app.js` logic on the new page.

