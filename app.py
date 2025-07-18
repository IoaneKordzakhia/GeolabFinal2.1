import os
from flask import Flask, render_template, request, redirect, url_for, session, flash

template_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')
app = Flask(__name__, template_folder=template_dir)
app.secret_key = 'supersecretkey'

products = [
    {
        'id': 1,
        'name': 'Test Product',
        'price': 99.99,
        'description': 'This is a test product.',
        'image_url': '/static/images/1.jpg',
        'images': [
            '/static/images/1.jpg',
            '/static/images/2.jpg'
        ]
    },
    {
        'id': 2,
        'name': 'Test Product2',
        'price': 15.99,
        'original_price': 2333.45,
        'description': 'On sale now!',
        'image_url': '/static/images/3.jpg',
        'images': [
            '/static/images/3.jpg',
            '/static/images/4.jpg',
            '/static/images/5.jpg'
        ]
    },
    {
        'id': 3,
        'name': 'Test Product2',
        'price': 23.45,
        'description': 'This is a test product.',
        'image_url': '/static/images/6.jpg',
        'images': [
            '/static/images/6.jpg',
            '/static/images/7.jpg',
            '/static/images/8.jpg',
            '/static/images/9.jpg'
        ]
    },
    {
        'id': 4,
        'name': 'Test Product2',
        'price': 40.45,
        'description': 'This is a test product.',
        'image_url': '/static/images/10.jpg',
        'images': [
            '/static/images/10.jpg',
            '/static/images/11.jpg',
        ]
    },
    {
        'id': 5,
        'name': 'Test Product2',
        'price': 70.45,
        'description': 'This is a test product.',
        'image_url': '/static/images/12.jpg',
        'images': [
            '/static/images/12.jpg',
            '/static/images/13.jpg',
            '/static/images/14.jpg',
            '/static/images/15.jpg'
        ]
    },
    {
        'id': 6,
        'name': 'Test Product2',
        'price': 75.45,
        'description': 'This is a test product.',
        'image_url': '/static/images/16.jpg',
        'images': [
            '/static/images/16.jpg',
            '/static/images/17.jpg',
            '/static/images/18.jpg',
            '/static/images/19.jpg'
        ]
    }
]

new_products = [
    {
        'id': 8,
        'name': 'New Cool Product',
        'price': 30.00,
        'description': 'Brand new cool product.',
        'image_url': '/static/images/23.jpg',
        'images': [
            '/static/images/23.jpg',
            '/static/images/24.jpg',
            '/static/images/25.jpg',
        ]
    },
    {
        'id': 9,
        'name': 'Another New Product',
        'price': 49.99,
        'description': 'Another new product in store.',
        'image_url': '/static/images/26.jpg',
        'images': [
            '/static/images/26.jpg',
            '/static/images/27.jpg',
            '/static/images/28.jpg',
            '/static/images/29.jpg'
        ]
    }
]

sales_products = [
    {
        'id': 2,
        'name': 'Test Product2',
        'price': 15,
        'original_price': 45.99,
        'description': 'On sale now!',
        'image_url': '/static/images/30.jpg',
        'images': [
            '/static/images/30.jpg',
            '/static/images/31.jpg',
            '/static/images/32.jpg',
        ]
    }
]

@app.route('/')
def index():
    return render_template('index.html', products=products)

@app.route('/products')
def product_list():
    return render_template('product.html', products=products)

@app.route('/product/<int:product_id>')
def product_detail(product_id):
    product = next((p for p in products if p['id'] == product_id), None)
    if not product:
        return "Product not found", 404
    return render_template('product_detail.html', product=product)

@app.route('/news')
def news():
    return render_template('news.html', new_products=new_products, sales_products=sales_products)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/cart')
def cart():
    cart_items = session.get('cart', [])
    for item in cart_items:
        item['total'] = round(item['price'] * item['quantity'], 2)
    grand_total = round(sum(item['total'] for item in cart_items), 2)
    return render_template('cart.html', cart_items=cart_items, grand_total=grand_total)

@app.route('/add_to_cart/<int:product_id>', methods=['POST'])
def add_to_cart(product_id):
    if 'user' not in session:
        flash('Please log in to add items to your cart.')
        return redirect(url_for('login'))

    product = next((p for p in products if p['id'] == product_id), None)
    if not product:
        flash('Product not found.')
        return redirect(url_for('index'))

    cart = session.get('cart', [])
    for item in cart:
        if item['id'] == product_id:
            item['quantity'] += 1
            break
    else:
        cart.append({'id': product['id'], 'name': product['name'], 'price': product['price'], 'quantity': 1})
    session['cart'] = cart
    flash(f'Added {product["name"]} to cart.')
    return redirect(url_for('cart'))

@app.route('/remove_from_cart/<int:product_id>', methods=['POST'])
def remove_from_cart(product_id):
    cart = session.get('cart', [])
    cart = [item for item in cart if item['id'] != product_id]
    session['cart'] = cart
    flash('Item removed from cart.')
    return redirect(url_for('cart'))

@app.route('/checkout', methods=['GET', 'POST'])
def checkout():
    if request.method == 'POST':
        session.pop('cart', None)
        flash("Successfully checked out! Thank you for your purchase.")
        return redirect(url_for('index'))
    return render_template('checkout.html')

@app.route('/search')
def search():
    query = request.args.get('query', '')
    results = [p for p in products if query.lower() in p['name'].lower()]
    return render_template('search_results.html', results=results, query=query)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username') or 'guest'
        session['user'] = {'username': username}
        flash(f'Welcome, {username}!')
        return redirect(url_for('index'))
    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        flash('Signup successful! Please log in.')
        return redirect(url_for('login'))
    return render_template('signup.html')

@app.route('/logout')
def logout():
    session.pop('user', None)
    flash('You have been logged out.')
    return redirect(url_for('index'))

@app.route('/services')
def services():
    return render_template('services.html')

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        message = request.form.get('message')
        flash('შეტყობინება წარმატებით გაიგზავნა! მადლობთ.')
        return redirect(url_for('contact'))
    return render_template('contact.html')

if __name__ == '__main__':
    app.run(debug=True)
