from flask import Blueprint, render_template, request, session, redirect, url_for, flash ,jsonify
from app.data_manager.session_manager import SessionManager
from app.data_manager.vendor import VendorObj
from app.data_manager.cart_manager import OrderManager
from config.config import JSONConfig
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from functools import wraps

config = JSONConfig("config.json")
engine = create_engine(f"sqlite:///{config.database_url.absolute()}")
Session = sessionmaker(bind=engine)
db_session = Session()

shop_bp = Blueprint("shop", __name__, url_prefix="/shop")
session_manager = SessionManager(db_session)

def vendor_selected(func):
    @wraps(func)
    def decorated_func(*args , **kwargs):
        if "vendor_id" not in session:
            return redirect(url_for(shop_bp.shop_home))
        return func(*args , **kwargs)
    return decorated_func

def get_or_create_session():
    """Ensures a session token exists in the user's session."""
    if "session_token" not in session:
        session["session_token"] = session_manager.create_new_session()
    return session["session_token"]

@shop_bp.before_request
def assign_session():
    """Assign a session token before handling any request."""
    get_or_create_session()


@shop_bp.route('/')
def shop_home():
    vendors = VendorObj.get_all_vendors(db_session=db_session)
    return render_template("shop/shops.html",vendors = vendors)
@shop_bp.route("/logout")
def logout():
    session.clear()
    return "Logged out"

@vendor_selected 
@shop_bp.route("/complete-payment")
def process_payment():
    cartdata =  session.get('cart' ,None)
    if  cartdata:
        total_cost =   cartdata['TotalCost']
        return render_template("shop/payment.html" , total_cost = total_cost)
    else:
        return redirect(url_for('shop.view_cart'))

@vendor_selected
@shop_bp.route("/<vendor_id>")
def vendor_products(vendor_id):
    """Displays products for a specific vendor."""
    session['vendor_id']=vendor_id
    vendor = VendorObj(vendor_id=vendor_id, db_session=db_session)
    products = vendor.get_product("vendor_id", vendor_id, occurrence="all")
    return render_template("shop/products2.html", products=products ,vendor=vendor.vendor_table)

@shop_bp.route("/product/<product_id>")
def specific_product(product_id):
    """Displays a specific product."""
    product = VendorObj(session.get("vendor_id"), db_session=db_session).get_product(
        product_key="id", value=product_id, occurrence="first"
    )
    return render_template("shop/specific_product.html", product=product)


@shop_bp.route("/add_to_cart", methods=["POST"])
def add_to_cart():
    session_token = session.get("session_token")
    if not session_token:
        return jsonify({"success": False, "error": "Session expired. Please refresh and try again."}), 400

    data = request.get_json()
    product_id = data.get("product_id")
    quantity = data.get("quantity")
    print(product_id , quantity)
    if not product_id or not quantity:
        return jsonify({"success": False, "error": "Invalid data"}), 400
    result = session_manager.add_to_cart(session_token, product_id, int(quantity))
    status = result['status']
    if status == "error":
         reason = result['reason']
         flash(f"Item not  added to cart{reason}", "error")
         return jsonify({"success": False})

    flash(f"Item added to cart!end{product_id} , {quantity}", "success")
    return jsonify({"success": True})





@shop_bp.route("/cart/remove", methods=["POST"])
def remove_from_cart():
    """Removes a product from the cart."""
    session_token = session["session_token"]
    data = request.get_json()

    product_id = data.get('product_id')
    print(product_id, data)
    if all ((session_manager ,product_id)):
        session_manager.remove_from_cart(session_token=session_token, product_id=product_id)
        flash("Item removed from cart!", "info")
    return jsonify({"success": False})

@shop_bp.route("/cart")
def view_cart(): 
    """Displays the user's cart."""
    session_token = session["session_token"]
    print("User is currently using sessin tokn "+session_token)
    cart_id = session_manager.get_cart(session_token)
    cart_items = session_manager.get_cartitems(cart_id=cart_id)
    
    return render_template("shop/cart.html", cart_items=cart_items)

@shop_bp.route("/update_cart", methods=["POST"])
def update_cart():
    """Handles updating cart item quantities via JavaScript."""
    session_token = session.get("session_token")
    if not session_token:
        return jsonify({"success": False, "message": "Session expired. Please refresh and try again."}), 400

    cart_id = session_manager.get_cart(session_token)
    if not cart_id:
        return jsonify({"success": False, "message": "Cart not found."}), 404

    data = request.get_json()
    quantities = data.get("quantities", {})

    for product_id, quantity in quantities.items():
        session_manager.update_cart_item(cart_id, int(product_id), int(quantity))

    return jsonify({"success": True, "message": "Cart updated successfully."})


@shop_bp.route("/checkout", methods=["GET", "POST"])
def checkout():
    """Handles the checkout process."""
    session_token = session.get("session_token")
    
    if not session_token:
        flash("Your session has expired. Please add items to the cart again.", "warning")
        return redirect(url_for("shop.vendor_products", vendor_id=session.get("vendor_id")))
    cart_summary = session_manager.get_cart_summary(session_token=session_token)
    session['cart']=cart_summary
    return render_template("shop/checkout2.html", cart_summary = cart_summary)

@vendor_selected
@shop_bp.route("/api-pay" , methods = ['POST'])
def api_process_payment():
    data = request.get_json()
    phone = data.get("phone")
    amount = data.get("amount")

    if phone[0] == "0":
        phone = phone.replace("0" , "254")


    amount = str(float(amount)/100)
    
    vendor_id = session['vendor_id']
    if not phone or not amount:
        return jsonify({"message": "Invalid data received."}), 400

    session_manager =  SessionManager(db_session=db_session)
    cart_id = session_manager.get_cart(session_token=session["session_token"])
    items = [{"product_id":i.product_id , 
              "quantity":i.quantity ,
                "price_at_purchase":i.product.price} for i in session_manager.get_cartitems(cart_id=cart_id)]
    

    order= OrderManager.create_new_order(db_session=db_session,
                                            session_tkn=session["session_token"],
                                            phone_number=phone,
                                            total_amount=amount,
                                            vendor_id=vendor_id,
                                            items=items
                                            )
    status = VendorObj(vendor_id=vendor_id , db_session=db_session).collect_payment(phone=phone,
                                                                                    amount=amount , orderid=order.order.session)

    if status:
        order.update_order(order.order.id , status =status)
    if status == 'paid':
        cart_status = session_manager.update_cart(cart_id=cart_id , attribute="is_active" , new_value=False)
     
        return jsonify({"message": "success"}) , 200
    return jsonify({"message": f"Payment request sent for ksh: {amount} to +{phone}."}) , 200



### ectra endpoints


@shop_bp.route("/search")
def search():
    return "Search Page (Placeholder)"

@shop_bp.route("/about")
def about():
    return "About Page (Placeholder)"

@shop_bp.route("/contact")
def contact():
    return "Contact Page (Placeholder)"

@shop_bp.route("/terms")
def terms():
    return "Terms & Conditions (Placeholder)"

@shop_bp.route("/privacy")
def privacy():
    return "Privacy Policy (Placeholder)"