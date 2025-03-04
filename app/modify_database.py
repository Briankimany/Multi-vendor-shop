from sqlalchemy.orm import Session
from models.vendor import Vendor, VendorPayout

def add_vendor(session: Session, name: str, email: str, phone: str, store_name: str, store_description: str = None):
    """
    Adds a new vendor to the database.
    """
    try:
        # Create Vendor instance
        new_vendor = Vendor(
            name=name,
            email=email,
            phone=phone,
            store_name=store_name,
            store_description=store_description,
            verified=False  # Default to unverified
        )
        
        session.add(new_vendor)
        session.flush()  # Get vendor.id before commit
        
        # Optional: Initialize payout tracking (if applicable)
        initial_payout = VendorPayout(
            vendor_id=new_vendor.id,
            amount=0.00,
            status='pending',
            transaction_ref=f"INIT-{new_vendor.id}"
        )
        session.add(initial_payout)
        
        session.commit()
        return new_vendor.id
    
    except Exception as e:
        session.rollback()
        raise e


from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from datetime import datetime

from app.models import Order, OrderItem, Payment, VendorPayout, Product

def process_transaction(session: Session, user_id, phone_number, vendor_id, items, payment_type, 
                        transaction_ref, amount_paid, payment_status):
    """
    Processes a new transaction.

    Args:
        session (Session): SQLAlchemy session object.
        user_id (int or None): User ID (None for guest users).
        phone_number (str): Customer's phone number.
        vendor_id (int): Vendor handling the order.
        items (list of dict): List of items (product_id, quantity, price_at_purchase).
        payment_type (str): 'pre-delivery' or 'payment-on-delivery'.
        transaction_ref (str): Unique payment reference.
        amount_paid (Decimal): Amount paid.
        payment_status (str): 'pending', 'successful', or 'failed'.

    Returns:
        dict: Transaction summary.
    """
    try:
        # Step 1: Create the Order
        order = Order(
            user_id=user_id,
            phone_number=phone_number,
            total_amount=sum(item["price_at_purchase"] * item["quantity"] for item in items),
            status="pending",
            payment_type=payment_type,
            vendor_id=vendor_id
        )
        session.add(order)
        session.flush()  # Get order ID before committing

        # Step 2: Add Order Items & Update Product Stock
        for item in items:
            product = session.query(Product).filter_by(id=item["product_id"]).first()
            if not product or product.stock < item["quantity"]:
                raise ValueError(f"Insufficient stock for product ID {item['product_id']}")

            product.stock -= item["quantity"]  # Reduce stock
            order_item = OrderItem(
                order_id=order.id,
                product_id=item["product_id"],
                quantity=item["quantity"],
                price_at_purchase=item["price_at_purchase"]
            )
            session.add(order_item)

        # Step 3: Record Payment
        payment = Payment(
            order_id=order.id,
            phone_number=phone_number,
            amount=amount_paid,
            status=payment_status,
            transaction_ref=transaction_ref
        )
        session.add(payment)

        # Step 4: Handle Vendor Payout if Payment is Successful
        if payment_status == "successful":
            vendor_payout = VendorPayout(
                vendor_id=vendor_id,
                amount=amount_paid,
                status="pending",  # Payout processing
                transaction_ref=transaction_ref
            )
            session.add(vendor_payout)
            order.status = "paid"

        # Step 5: Commit Transaction
        session.commit()

        return {
            "order_id": order.id,
            "status": order.status,
            "payment_status": payment.status,
            "total_amount": order.total_amount,
            "items": items
        }

    except IntegrityError:
        session.rollback()
        raise ValueError("Database integrity error occurred.")
    
    except Exception as e:
        session.rollback()
        raise ValueError(f"Transaction failed: {str(e)}")
