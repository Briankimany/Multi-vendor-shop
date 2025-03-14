from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models.base import Base
from config.config import JSONConfig
from sqlalchemy import text

config = JSONConfig("config.json")

DATABASE_URL = f"sqlite:///{config.database_url.absolute()}"
engine = create_engine(DATABASE_URL, echo=False)

SessionLocal = sessionmaker(bind=engine)

def reset_table(table_name: str):
    """Drops the specified table and recreates the database schema."""
    with SessionLocal() as session:
        try:
            # Drop the table
            session.execute(text(f"DROP TABLE IF EXISTS {table_name}"))
            session.commit()
            print(f"Table '{table_name}' dropped successfully.")

            # Recreate all tables (ensures dependencies are handled)
            Base.metadata.create_all(engine)
            print("Database schema recreated.")

        except Exception as e:
            session.rollback()
            print(f"Error resetting table {table_name}: {e}")

# reset_table("order_items")
# reset_table("carts")

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

