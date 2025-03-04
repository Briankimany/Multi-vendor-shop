from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models.base import Base
from config.config import JSONConfig

config = JSONConfig("config.json")

DATABASE_URL = f"sqlite:///{config.database_url.absolute()}"
engine = create_engine(DATABASE_URL, echo=False)

SessionLocal = sessionmaker(bind=engine)

def init_db():
    from models.session_tracking import SessionTracking
    from models import (
        user_profile,
        vendor,
        product,
        order,
        cart,
        payment,
        wishlist,
        discount,
        order_item,
        
    )  
    
    Base.metadata.create_all(bind=engine)
init_db()