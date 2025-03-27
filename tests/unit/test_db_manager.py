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
engine = create_engine(f"sqlite:///{config.database_url.absolute()}")
Session = sessionmaker(bind=engine)
session = Session()


vendor = Vendor(
    name="Tech Haven",
    email="tech@haven.com",
    phone="+1234567890",
    store_name="Tech Haven Store",
    store_description="Your one-stop shop for all tech gadgets.",
    verified=True,
    store_logo = "https://img401.picturelol.com/th/67769/9rxu5xjquw3l.jpg",
    payment_type =  'pre-delivery'
)
session.add(vendor)
session.commit()

vendor2 = Vendor(
    name="Fashion Fiesta",
    email="support@fashionfiesta.com",
    phone="+1987654321",
    store_name="Fashion Fiesta",
    store_description="Trendy and stylish clothing for all occasions.",
    verified=True,
    store_logo="https://img401.picturelol.com/th/67769/9rxu5xjquw3l.jpg",
    payment_type='pre-delivery'
)

vendor3 = Vendor(
    name="Home Essentials",
    email="support@homeessentials.com",
    phone="+1122334455",
    store_name="Home Essentials",
    store_description="Everything you need to make your home comfortable and stylish.",
    verified=True,
    store_logo="https://img401.picturelol.com/th/67769/9rxu5xjquw3l.jpg",
    payment_type='pre-delivery'
)

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


session.add_all([vendor , vendor2 , vendor3 , vendor4])
session.commit()




