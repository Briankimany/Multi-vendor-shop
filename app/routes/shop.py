from flask import Blueprint, render_template, request, session, redirect, url_for, flash ,jsonify
from app.data_manager.session_manager import SessionManager
from app.data_manager.vendor import VendorObj
from app.models.cart import Cart as CartModel
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
@shop_bp.route("/<vendor_id>")
def vendor_products(vendor_id):
    """Displays products for a specific vendor."""
    session['vendor_id']=vendor_id
    vendor = VendorObj(vendor_id=vendor_id, db_session=db_session)
    products = vendor.get_product("vendor_id", vendor_id, occurrence="all")
    print(products)
    return render_template("shop/products.html", products=products)

@shop_bp.route("/product/<product_id>")
def specific_product(product_id):
    """Displays a specific product."""
    product = VendorObj(session.get("vendor_id"), db_session=db_session).get_product(
        product_key="id", value=product_id, occurrence="first"
    )
    return render_template("shop/specific_product.html", product=product)

@shop_bp.route("/cart/add/<product_id>", methods=["POST"])
def add_to_cart(product_id):
    """Adds a product to the user's cart."""
    session_token = session["session_token"]
    
    quantity = int(request.form.get("quantity", 1))
    session_manager.add_to_cart(session_token, product_id, quantity)
    flash("Item added to cart!", "success")
    return redirect(request.referrer or url_for("shop.vendor_products", vendor_id=session.get("vendor_id")))

@shop_bp.route("/cart/remove/<product_id>", methods=["POST"])
def remove_from_cart(product_id):
    """Removes a product from the cart."""
    session_token = session["session_token"]
    session_manager.remove_from_cart(session_token, product_id)
    flash("Item removed from cart!", "info")
    return redirect(url_for("shop.view_cart"))

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
    return render_template("shop/checkout.html", cart_summary = cart_summary)
