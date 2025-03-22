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
config = JSONConfig("config.json")
# Setup the database engine and session
engine = create_engine(f"sqlite:///{config.database_url.absolute()}")
Session = sessionmaker(bind=engine)
session = Session()

vendor4 = Vendor(
    name="Tech Solutions Hub",
    email="support@techsolutionshub.com",
    phone="+1234567894",
    store_name="Tech Solutions Hub",
    store_description="Professional tech services including software installation, AI assistance, and project development.",
    verified=True,
    store_logo="https://img401.picturelol.com/th/67769/9rxu5xjquw3l.jpg",
    payment_type='pre-delivery'
)
session.add(vendor4)
session.commit()


# vendor2 = Vendor(
#     name="Fashion Fiesta",
#     email="support@fashionfiesta.com",
#     phone="+1987654321",
#     store_name="Fashion Fiesta",
#     store_description="Trendy and stylish clothing for all occasions.",
#     verified=True,
#     store_logo="https://img401.picturelol.com/th/67769/9rxu5xjquw3l.jpg",
#     payment_type='pre-delivery'
# )
# session.add(vendor2)
# session.commit()

# products2 = [
#     Product(vendor_id=vendor2.id, name="Denim Jacket", description="Classic blue denim jacket for casual wear.", price=49.99, stock=30, category="Clothing", image_url="https://img401.picturelol.com/th/67769/9rxu5xjquw3l.jpg"),
#     Product(vendor_id=vendor2.id, name="Leather Boots", description="High-quality leather boots for all seasons.", price=89.99, stock=20, category="Footwear", image_url="https://img401.picturelol.com/th/67769/9rxu5xjquw3l.jpg"),
#     Product(vendor_id=vendor2.id, name="Sunglasses", description="UV-protection stylish sunglasses.", price=29.99, stock=40, category="Accessories", image_url="https://img401.picturelol.com/th/67769/9rxu5xjquw3l.jpg"),
#     Product(vendor_id=vendor2.id, name="Sports Hoodie", description="Lightweight sports hoodie for workouts.", price=39.99, stock=35, category="Clothing", image_url="https://img401.picturelol.com/th/67769/9rxu5xjquw3l.jpg"),
#     Product(vendor_id=vendor2.id, name="Running Shoes", description="Comfortable and stylish running shoes.", price=79.99, stock=25, category="Footwear", image_url="https://img401.picturelol.com/th/67769/9rxu5xjquw3l.jpg"),
#     Product(vendor_id=vendor2.id, name="Elegant Watch", description="Luxury stainless steel wristwatch.", price=149.99, stock=15, category="Accessories", image_url="https://img401.picturelol.com/th/67769/9rxu5xjquw3l.jpg"),
#     Product(vendor_id=vendor2.id, name="Backpack", description="Durable and spacious travel backpack.", price=59.99, stock=30, category="Accessories", image_url="https://img401.picturelol.com/th/67769/9rxu5xjquw3l.jpg"),
#     Product(vendor_id=vendor2.id, name="Formal Suit", description="Tailored-fit formal suit for business and weddings.", price=249.99, stock=10, category="Clothing", image_url="https://img401.picturelol.com/th/67769/9rxu5xjquw3l.jpg"),
#     Product(vendor_id=vendor2.id, name="Casual Sneakers", description="Trendy sneakers for everyday use.", price=69.99, stock=25, category="Footwear", image_url="https://img401.picturelol.com/th/67769/9rxu5xjquw3l.jpg"),
#     Product(vendor_id=vendor2.id, name="Designer Handbag", description="Stylish handbag with multiple compartments.", price=199.99, stock=18, category="Accessories", image_url="https://img401.picturelol.com/th/67769/9rxu5xjquw3l.jpg")
# ]

# session.add_all(products2)
# session.commit()

# vendor3 = Vendor(
#     name="Home Essentials",
#     email="support@homeessentials.com",
#     phone="+1122334455",
#     store_name="Home Essentials",
#     store_description="Everything you need to make your home comfortable and stylish.",
#     verified=True,
#     store_logo="https://img401.picturelol.com/th/67769/9rxu5xjquw3l.jpg",
#     payment_type='pre-delivery'
# )


# products3 = [
#     Product(vendor_id=vendor3.id, name="Air Fryer", description="Oil-free cooking with a high-capacity air fryer.", price=129.99, stock=15, category="Kitchen Appliances", image_url="https://img401.picturelol.com/th/67769/9rxu5xjquw3l.jpg"),
#     Product(vendor_id=vendor3.id, name="Vacuum Cleaner", description="Powerful cordless vacuum cleaner for deep cleaning.", price=199.99, stock=10, category="Home Appliances", image_url="https://img401.picturelol.com/th/67769/9rxu5xjquw3l.jpg"),
#     Product(vendor_id=vendor3.id, name="Electric Kettle", description="Fast boiling electric kettle with auto shut-off.", price=49.99, stock=30, category="Kitchen Appliances", image_url="https://img401.picturelol.com/th/67769/9rxu5xjquw3l.jpg"),
#     Product(vendor_id=vendor3.id, name="Smart LED Bulbs", description="WiFi-controlled LED bulbs with color changing options.", price=24.99, stock=50, category="Home Decor", image_url="https://img401.picturelol.com/th/67769/9rxu5xjquw3l.jpg"),
#     Product(vendor_id=vendor3.id, name="Luxury Bedsheets", description="Soft and comfortable high-thread count bedsheets.", price=69.99, stock=20, category="Bedding", image_url="https://img401.picturelol.com/th/67769/9rxu5xjquw3l.jpg"),
#     Product(vendor_id=vendor3.id, name="Non-Stick Cookware Set", description="Durable non-stick pots and pans for easy cooking.", price=149.99, stock=12, category="Kitchen", image_url="https://img401.picturelol.com/th/67769/9rxu5xjquw3l.jpg"),
#     Product(vendor_id=vendor3.id, name="Wall Clock", description="Elegant decorative wall clock for your living room.", price=39.99, stock=25, category="Home Decor", image_url="https://img401.picturelol.com/th/67769/9rxu5xjquw3l.jpg"),
#     Product(vendor_id=vendor3.id, name="Standing Fan", description="Adjustable-height standing fan with multiple speed settings.", price=89.99, stock=18, category="Home Appliances", image_url="https://img401.picturelol.com/th/67769/9rxu5xjquw3l.jpg"),
#     Product(vendor_id=vendor3.id, name="Electric Blanket", description="Stay warm with this energy-efficient electric blanket.", price=79.99, stock=15, category="Bedding", image_url="https://img401.picturelol.com/th/67769/9rxu5xjquw3l.jpg"),
#     Product(vendor_id=vendor3.id, name="Air Purifier", description="Breathe clean air with this HEPA filter air purifier.", price=249.99, stock=10, category="Home Appliances", image_url="https://img401.picturelol.com/th/67769/9rxu5xjquw3l.jpg")
# ]

# session.add_all(products3)
# session.commit()


# def newentry():
#     # Create a new vendor

#     vendor = Vendor(
#         name="Tech Haven",
#         email="tech@haven.com",
#         phone="+1234567890",
#         store_name="Tech Haven Store",
#         store_description="Your one-stop shop for all tech gadgets.",
#         verified=True,
#         store_logo = "https://img401.picturelol.com/th/67769/9rxu5xjquw3l.jpg",
#         payment_type =  'pre-delivery'
#     )
#     session.add(vendor)
#     session.commit()

#     # Add a new product for the vendor
#     product = Product(
#         vendor_id=vendor.id,
#         name="Gaming Laptop",
#         description="High-performance gaming laptop with RTX 4090",
#         price=2499.99,
#         stock=10,
#         category="Electronics",
#         image_url="https://img401.picturelol.com/th/67769/9rxu5xjquw3l.jpg",
#         preview_url="https://example.com/laptop_preview.mp4",
       
#     )
#     session.add(product)
#     session.commit()

#     # Create a new user
#     user = UserProfile(
#         name="Alex Johnson",
#         email="alex@example.com",
#         phone="+1987654321",
#         password_hash="hashedpassword123"
#     )
#     session.add(user)
#     session.commit()


#     cart = Cart(user_id=user.id , session_tkn ="akdflsjdflsjdfjlsdjfitj")
#     session.add(cart)
#     session.commit()

#     cart_item = CartItem(cart_id=cart.id, product_id=product.id, quantity=1)
#     session.add(cart_item)
#     session.commit()

#     # Create a new order
#     order = Order(
#         user_id=user.id,
#         phone_number=user.phone,
#         total_amount=product.price,
#         status="pending",
#         payment_type="pre-delivery",
#         vendor_id=vendor.id,
#         session = "akdflsjdflsjdfjlsdjfitj"
#     )
#     session.add(order)
#     session.commit()

#     # Add order item
#     order_item = OrderItem(
#         order_id=order.id,
#         product_id=product.id,
#         quantity=1,
#         price_at_purchase=product.price
#     )
#     session.add(order_item)
#     session.commit()

#     # Process payment
#     payment = Payment(
#         order_id=order.id,
#         phone_number=user.phone,
#         amount=order.total_amount,
#         status="successful",
#         transaction_ref="TRANS123456"
#     )
#     session.add(payment)
#     session.commit()

#     # Process vendor payout
#     payout = VendorPayout(
#         vendor_id=vendor.id,
#         amount=order.total_amount,
#         status="pending",
#         transaction_ref="PAYOUT987654"
#     )
#     session.add(payout)
#     session.commit()

#     # Fetch and print results
#     print("Vendor:", session.query(Vendor).first())
#     print("Product:", session.query(Product).first())
#     print("User:", session.query(UserProfile).first())
#     print("Cart:", session.query(Cart).first())
#     print("Cart Item:", session.query(CartItem).first())
#     print("Order:", session.query(Order).first())
#     print("Order Item:", session.query(OrderItem).first())
#     print("Payment:", session.query(Payment).first())
#     print("Vendor Payout:", session.query(VendorPayout).first())


# newentry()
# ## add extraservices
# from app.data_manager.vendor import VendorObj
# # Step 1: Retrieve the vendor (assuming we have the vendor_id)
# VendorObj = VendorObj(vendor_id=1, db_session=session)

# # Step 2: Add new products
# new_products = [
#     {"name": "Phone A", "price": 500.00, "product_type": 0, "stock": 20, "category": "Smartphones" , 'image_url':"https://img401.picturelol.com/th/67769/9rxu5xjquw3l.jpg"},
#     {"name": "Phone B", "price": 1200.00, "product_type": 0, "stock": 15, "category": "Smartphones" , 'image_url':"https://img401.picturelol.com/th/67769/9rxu5xjquw3l.jpg"},
#     {"name": "Phone C", "price": 300.00, "product_type": 0, "stock": 30, "category": "Smartphones" , 'image_url':"https://img401.picturelol.com/th/67769/9rxu5xjquw3l.jpg"},
#     {"name": "Software Installation Service", "price": 50.00, "product_type": 1, "category": "Services" , 'image_url':"https://img401.picturelol.com/th/67769/9rxu5xjquw3l.jpg"},
#     {"name": "Device Repair Service", "price": 100.00, "product_type": 1, "category": "Services" , 'image_url':"https://img401.picturelol.com/th/67769/9rxu5xjquw3l.jpg"},
# ]

# # # Add products to the vendor
# for product in new_products:
#     VendorObj.add_product(**product)

# # Step 3: Increase gaming laptop stock
# # Assuming we know the product_id of the gaming laptop
# gaming_laptop_id = 1
# VendorObj.modify_products([
#     {"id": gaming_laptop_id, "data": {"stock": 50}}  # Increase stock to 50
# ])

