from sqlalchemy import Column, Integer, String, Numeric, ForeignKey, TIMESTAMP
from sqlalchemy.sql import func

from .base import Base
from .user_profile import UserProfile 
from .vendor import Vendor

class Order(Base):
    __tablename__ = 'orders'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey(UserProfile.id), nullable=True)
    phone_number = Column(String, nullable=False)
    total_amount = Column(Numeric(10, 2), nullable=False)
    status = Column(String, default='pending')  # pending, paid, canceled
    payment_type = Column(String)  # pre-delivery or payment-on-delivery
    vendor_id = Column(Integer, ForeignKey(Vendor.id), nullable=False)  # Correct foreign key reference
    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())
