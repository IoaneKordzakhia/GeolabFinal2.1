import os
from flask import Flask, render_template, request, redirect, url_for, session

template_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')
app = Flask(__name__, template_folder=template_dir)
app.secret_key = 'supersecretkey'

# Dummy product data
products = [
    {'id': 1, 'name': 'FDSFSDFS', 'price': 69.00, 'description': 'lamazi.', 'image_url': '/static/shirt.jpg'},
    {'id': 2, 'name': 'FDSFSDFDS', 'price': 50.00, 'description': 'Run in style.', 'image_url': '/static/sneakers.jpg'},
    {'id': 3, 'name': 'DASDASDSA', 'price': 150.00, 'description': 'Track your time smartly.', 'image_url': '/static/watch.jpg'},
]

# Home Page
@app.route('/')
def index():
    return render_template('index.html', products=products)

# Product List Page
@app.route('/products')
def product_list():
    return render_template('product.html', products=products)

# Product Detail Page
@app.route('/product/<int:product_id>')
def product_detail(product_id):
    product = next((p for p in products if p['id'] == product_id), None)
    return render_template('product_detail.html', product=product)

# About Page
@app.route('/about')
def about():
    return render_template('about.html')

# Cart Page
@app.route('/cart')
def cart():
    cart_items = session.get('cart', [])
    total = sum(item['price'] * item['quantity'] for item in cart_items)
    for item in cart_items:
        item['total'] = item['price'] * item['quantity']
    return render_template('cart.html', cart_items=cart_items, grand_total=total)

# Add to Cart
@app.route('/add_to_cart/<int:product_id>', methods=['POST'])
def add_to_cart(product_id):
    product = next((p for p in products if p['id'] == product_id), None)
    if not product:
        return redirect(url_for('index'))

    cart = session.get('cart', [])
    for item in cart:
        if item['id'] == product_id:
            item['quantity'] += 1
            break
    else:
        cart.append({'id': product['id'], 'name': product['name'], 'price': product['price'], 'quantity': 1})
    session['cart'] = cart
    return redirect(url_for('cart'))

# Remove from Cart
@app.route('/remove_from_cart/<int:product_id>', methods=['POST'])
def remove_from_cart(product_id):
    cart = session.get('cart', [])
    cart = [item for item in cart if item['id'] != product_id]
    session['cart'] = cart
    return redirect(url_for('cart'))

# Checkout Page
@app.route('/checkout', methods=['GET', 'POST'])
def checkout():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        address = request.form.get('address')
        card_number = request.form.get('card_number')
        exp_date = request.form.get('exp_date')
        cvc = request.form.get('cvc')

        # Payment validation logic goes here (not implemented)
        session.pop('cart', None)  # Clear cart after checkout
        return render_template('confirmation.html', name=name)

    return render_template('checkout.html')

# Search
@app.route('/search')
def search():
    query = request.args.get('query', '')
    results = [p for p in products if query.lower() in p['name'].lower()]
    return render_template('search_results.html', results=results, query=query)

# Login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        session['user'] = {'username': request.form.get('username', 'guest')}
        return redirect(url_for('index'))
    return render_template('login.html')

# Signup
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        return redirect(url_for('login'))
    return render_template('signup.html')

# Logout
@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('index'))

# Run the app
if __name__ == '__main__':
    app.run()
