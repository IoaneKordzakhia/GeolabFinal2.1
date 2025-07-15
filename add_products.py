from app import db, Product  # Import db and Product model from app.py

# Create a list of products you want to add
products = [
    {
        "name": "Product 1", 
        "description": "Description of product 1", 
        "price": 10.0, 
        "image": "images/download.jpg",  # Reference to the image
        "extra_images": ["images/product1_1.jpg", "images/product1_2.jpg"], 
        "sizes": ["S", "M", "L"]
    },
    {"name": "Product 2", "description": "Description of product 2", "price": 20.0, 
     "image": "images/product2.jpg", "extra_images": ["images/product2_1.jpg"], 
     "sizes": ["M", "L"]},
]

# Set up the Flask app context to access db
from app import app  # Make sure to import the app from your app.py

with app.app_context():  # This ensures the app context is available
    for product_data in products:
        # Create product objects
        product = Product(
            name=product_data["name"],
            description=product_data["description"],
            price=product_data["price"],
            image=product_data["image"],  # Correct image path here
            extra_images=product_data["extra_images"],
            sizes=product_data["sizes"]
        )

        # Add product to the database
        db.session.add(product)

    # Commit all changes to the database
    db.session.commit()
    print("Products added successfully!")
