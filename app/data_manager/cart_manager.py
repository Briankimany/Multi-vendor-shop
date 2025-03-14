
from sqlalchemy.orm import Session
from app.models.order import Order
from app.models.order_item import OrderItem
from .session_manager import SessionManager
from .database_index import Database

from sqlalchemy.exc import SQLAlchemyError

class OrderManager:
    def __init__(self, db_session: Session, order_id):
        """
        Initializes an `OrderManager` instance with an order.

        Args:
            db_session (Session): The active SQLAlchemy database session.
            order_id : The ID of the order to be managed or an instance of Order

        Attributes:
            db_session (Session): The SQLAlchemy session for database operations.
            order (Order o): The order object if found
        """
        self.db_session = db_session
        self.order = self.db_session.query(Order).where(Order.id == order_id).first() if not isinstance(order_id , Order) else order_id

    @staticmethod
    def get_order_by_session_tkn(db_session:Session , session_tkn):
        """
        Retrieves an order associated with a given session token.

        Args:
            db_session (Session): The active SQLAlchemy database session.
            session_tkn (str): The session token linked to the order.

        Returns:
            Order or None: The order object if found, otherwise None.
         """
        return db_session.query(Order).filter(Order.session == session_tkn, Order.status != "paid" ,Order.status != "canceled").first()

       
    @staticmethod
    def create_new_order(db_session:Session, session_tkn, phone_number=None, 
                         total_amount=None, payment_type=None, vendor_id=None, items=[], user_id=None) :
        """
        Creates a new order if none exists for the given session token and inserts associated order items.

        If no order is found for the given session token, a new order is created in the `Order` table.
        The method then inserts multiple related order items into the `OrderItem` table.

        Args:
            db_session (Session): The active SQLAlchemy database session.
            session_tkn (str): The session token associated with the order.
            phone_number (str, optional): The phone number of the customer placing the order.
            total_amount (Decimal, optional): The total cost of the order.
            payment_type (str, optional): The type of payment, either "pre-delivery" or "payment-on-delivery".
            vendor_id (int, optional): The ID of the vendor fulfilling the order.
            items (list[dict], optional): A list of dictionaries, each containing:
                - product_id (int): ID of the ordered product.
                - quantity (int): Number of units ordered.
                - price_at_purchase (Decimal): Price per unit at the time of purchase.
            user_id (int, optional): The user ID if the customer is registered.

        Returns:
            OrderManager: An instance of `OrderManager` managing the newly created order.
            None: if creation fails.
        """
        order = OrderManager.get_order_by_session_tkn(db_session=db_session,session_tkn=session_tkn)
    
        try:
            if not order:
                if not user_id:
                    user_id = SessionManager.get_userid_associated_with_tkn(db_session=db_session,session_token=session_tkn)
                if not payment_type:
                    vendor = Database(session=db_session).get_vendor(vendor_id=vendor_id)
                    payment_type = vendor.payment_type
                    
                new_order = Order(
                    session=session_tkn,
                    user_id=user_id,
                    phone_number=phone_number,
                    total_amount=total_amount,
                    status="pending",  # Default status
                    payment_type=payment_type,
                    vendor_id=vendor_id
                )
                db_session.add(new_order)
                db_session.commit()  

            
                order_items = [
                    OrderItem(
                        order_id=new_order.id,
                        product_id=item["product_id"],
                        quantity=item["quantity"],
                        price_at_purchase=item["price_at_purchase"]
                    )
                    for item in items
                ]
                db_session.add_all(order_items)
                db_session.commit()
                order = new_order
            return OrderManager(db_session=db_session , order_id=order)
        except SQLAlchemyError as e:
            db_session.rollback()
            print(f"Database Error: {e}")
            return None
        
    def get_order_details(self, include_items=True):
        """
        Retrieves detailed information about an order.

        Args:
            include_items (bool, optional): Whether to include order item details. Defaults to True.

        Returns:
            dict or None: A dictionary containing order details, or None if the order does not exist.
            
            Structure:
            {
                "order_id": int,
                "user_id": int or None,
                "phone_number": str ,
                "total_amount": float,
                "status": str,
                "payment_type": str,
                "vendor_id": int ,
                "created_at": datetime,
                "updated_at": datetime,
                "items": [
                    {
                        "product_id": int,
                        "quantity": int,
                        "price_at_purchase": float
                    },
                    ...
                ]  # Only if `include_items` is True
            }
        """

        if not self.order:
            return None
        
        order_data = {
            "order_id": self.order.id,
            "user_id": self.order.user_id,
            "phone_number": self.order.phone_number,
            "total_amount": float(self.order.total_amount),
            "status": self.order.status,
            "payment_type": self.order.payment_type,
            "vendor_id": self.order.vendor_id,
            "created_at": self.order.created_at,
            "updated_at": self.order.updated_at,
        }

        if include_items:
            order_data["items"] = [
                {
                    "product_id": item.product_id,
                    "quantity": item.quantity,
                    "price_at_purchase": float(item.price_at_purchase),
                }
                for item in self.db_session.query(OrderItem).filter_by(order_id=self.order.id).all()
            ]

        return order_data

    def delete_order(self):
        """ Delete the order and its associated items """
        if not self.order:
            return False

        try:
            self.db_session.query(OrderItem).filter_by(order_id=self.order.id).delete()
            self.db_session.delete(self.order)
            self.db_session.commit()
            self.order = None
            return True
        except SQLAlchemyError as e:
            self.db_session.rollback()
            print(f"Database Error: {e}")
            return False
        
    def update_order(self, order_id: int, **kwargs):
        """
        Updates specified attributes of an existing order.

        This method modifies provided attributes of an order in the `Order` table, ensuring only valid fields are updated.

        Args:
            order_id (int): The ID of the order to be updated.
            **kwargs: Key-value pairs representing the fields to be updated. 
                    Valid keys include:
                    - phone_number (str)
                    - total_amount (Decimal)
                    - status (str) -(pending, paid, canceled)
                    - payment_type (str)
                    - vendor_id (int)

        Returns:
            bool: True if the update is successful, False otherwise.
         """
        if not self.order or self.order.id != order_id:
            return False

        try:
            for key, value in kwargs.items():
                if hasattr(self.order, key):
                    setattr(self.order, key, value)

            self.db_session.commit()
            return True
        except SQLAlchemyError as e:
            self.db_session.rollback()
            print(f"Database Error: {e}")
            return False

