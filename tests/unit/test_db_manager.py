from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from app.models.base import Base
from app.models.vendor import Vendor, VendorPayout
from app.models.product import Product
from app.models.user_profile import UserProfile
from app.models.cart import Cart, CartItem
from app.models.order import Order
from app.models.order_item import OrderItem
from app.models.payment import Payment

from config.config import JSONConfig
config = JSONConfig('config.json')
# Setup the database engine and session
engine = create_engine(f"sqlite:///{config.database_url.absolute()}")
Session = sessionmaker(bind=engine)
session = Session()


def newentry():
    # Create a new vendor

    vendor = Vendor(
        name="Tech Haven",
        email="tech@haven.com",
        phone="+1234567890",
        store_name="Tech Haven Store",
        store_description="Your one-stop shop for all tech gadgets.",
        verified=True,
        store_logo = "https://img401.picturelol.com/th/67769/9rxu5xjquw3l.jpg"
    )
    session.add(vendor)
    session.commit()

    # Add a new product for the vendor
    product = Product(
        vendor_id=vendor.id,
        name="Gaming Laptop",
        description="High-performance gaming laptop with RTX 4090",
        price=2499.99,
        stock=10,
        category="Electronics",
        image_url="https://example.com/laptop.jpg",
        preview_url="https://example.com/laptop_preview.mp4"
    )
    session.add(product)
    session.commit()

    # Create a new user
    user = UserProfile(
        name="Alex Johnson",
        email="alex@example.com",
        phone="+1987654321",
        password_hash="hashedpassword123"
    )
    session.add(user)
    session.commit()


    cart = Cart(user_id=user.id)
    session.add(cart)
    session.commit()

    cart_item = CartItem(cart_id=cart.id, product_id=product.id, quantity=1)
    session.add(cart_item)
    session.commit()

    # Create a new order
    order = Order(
        user_id=user.id,
        phone_number=user.phone,
        total_amount=product.price,
        status="pending",
        payment_type="pre-delivery",
        vendor_id=vendor.id
    )
    session.add(order)
    session.commit()

    # Add order item
    order_item = OrderItem(
        order_id=order.id,
        product_id=product.id,
        quantity=1,
        price_at_purchase=product.price
    )
    session.add(order_item)
    session.commit()

    # Process payment
    payment = Payment(
        order_id=order.id,
        phone_number=user.phone,
        amount=order.total_amount,
        status="successful",
        transaction_ref="TRANS123456"
    )
    session.add(payment)
    session.commit()

    # Process vendor payout
    payout = VendorPayout(
        vendor_id=vendor.id,
        amount=order.total_amount,
        status="pending",
        transaction_ref="PAYOUT987654"
    )
    session.add(payout)
    session.commit()

    # Fetch and print results
    print("Vendor:", session.query(Vendor).first())
    print("Product:", session.query(Product).first())
    print("User:", session.query(UserProfile).first())
    print("Cart:", session.query(Cart).first())
    print("Cart Item:", session.query(CartItem).first())
    print("Order:", session.query(Order).first())
    print("Order Item:", session.query(OrderItem).first())
    print("Payment:", session.query(Payment).first())
    print("Vendor Payout:", session.query(VendorPayout).first())


newentry()
## add extraservices
from app.data_manager.vendor import VendorObj
# Step 1: Retrieve the vendor (assuming we have the vendor_id)
VendorObj = VendorObj(vendor_id=1, db_session=session)

# Step 2: Add new products
new_products = [
    {"name": "Phone A", "price": 500.00, "product_type": 0, "stock": 20, "category": "Smartphones" , 'image_url':"https://img401.picturelol.com/th/67769/9rxu5xjquw3l.jpg"},
    {"name": "Phone B", "price": 1200.00, "product_type": 0, "stock": 15, "category": "Smartphones" , 'image_url':"https://img401.picturelol.com/th/67769/9rxu5xjquw3l.jpg"},
    {"name": "Phone C", "price": 300.00, "product_type": 0, "stock": 30, "category": "Smartphones" , 'image_url':"https://img401.picturelol.com/th/67769/9rxu5xjquw3l.jpg"},
    {"name": "Software Installation Service", "price": 50.00, "product_type": 1, "category": "Services" , 'image_url':"https://img401.picturelol.com/th/67769/9rxu5xjquw3l.jpg"},
    {"name": "Device Repair Service", "price": 100.00, "product_type": 1, "category": "Services" , 'image_url':"https://img401.picturelol.com/th/67769/9rxu5xjquw3l.jpg"},
]

# # Add products to the vendor
for product in new_products:
    VendorObj.add_product(**product)

# Step 3: Increase gaming laptop stock
# Assuming we know the product_id of the gaming laptop
gaming_laptop_id = 1
VendorObj.modify_products([
    {"id": gaming_laptop_id, "data": {"stock": 50}}  # Increase stock to 50
])

