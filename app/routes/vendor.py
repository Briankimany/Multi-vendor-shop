from flask import Blueprint, render_template, request, redirect, url_for, flash, session

from app.data_manager.vendor import VendorObj
from config.config import JSONConfig

from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

config = JSONConfig('config.json')

engine = create_engine(f"sqlite:///{config.database_url.absolute()}")
Session = sessionmaker(bind=engine)
db_session = Session()
vendor_bp = Blueprint("vendor", __name__, url_prefix="/vendor")

@vendor_bp.route("/login")
def login():
    session['vendor_id'] = 1
    return "logged in "
@vendor_bp.route("/logout")
def logout():
    session.clear()
    return "Logged out"
@vendor_bp.route("/register")
def register():
    session['vendor_id'] = 1
    return "logged in "

@vendor_bp.route("/")
def vendorhome():
    return render_template("vendor/home.html")


@vendor_bp.route("/dashboard")
def dashboard():
    if "vendor_id" not in session:
        return redirect(url_for("vendor.login"))
    vendor = VendorObj(session['vendor_id'], db_session=db_session)
    return render_template(
        "vendor/dashboard2.html",
        summary=vendor.get_dashboard_data(),
        recent_orders=vendor.get_recent_orders(),
        low_stock_products=vendor.get_low_stock_products(),
    )
@vendor_bp.route("/add_product", methods=["GET", "POST"])
def add_product():
    if "vendor_id" not in session:
        return redirect(url_for("vendor.login"))
    
    if request.method == "POST":
        name = request.form.get("name")
        description = request.form.get("description")
        price = request.form.get("price", type=float)
        stock = request.form.get("stock", type=int)
        category = request.form.get("category")
        image_url = request.form.get("image_url")
        preview_url = request.form.get("preview_url")
        product_type = request.form.get("product_type", type=int)
        
        vendor = VendorObj(session["vendor_id"], db_session)
        vendor.add_product(name=name, description=description, price=price, stock=stock, category=category, image_url=image_url, preview_url=preview_url, product_type=product_type)
        
        flash("Product added successfully!", "success")
        return redirect(url_for("vendor.dashboard"))
    
    return render_template("vendor/add_product.html")

@vendor_bp.route("/edit_product/<int:product_id>", methods=["GET", "POST"])
def edit_product(product_id):
    if "vendor_id" not in session:
        return redirect(url_for("vendor.login"))
    
    vendor = VendorObj(session["vendor_id"], db_session)
    product = vendor.get_product(product_key='id' , value=product_id)
    if request.method == "POST":
        updated_data = {
            "name": request.form.get("name"),
            "description": request.form.get("description"),
            "price": request.form.get("price", type=float),
            "stock": request.form.get("stock", type=int),
            "category": request.form.get("category"),
            "image_url": request.form.get("image_url"),
            "preview_url": request.form.get("preview_url"),
        }
        vendor.modify_products([{"id": product_id, "data": updated_data}])
        
        flash("Product updated successfully!", "success")
        return redirect(url_for("vendor.dashboard"))
    
    return render_template("vendor/edit_product.html", product_id=product_id , product=product )

@vendor_bp.route("/delete_product/<int:product_id>", methods=["POST"])
def delete_product(product_id):
    if "vendor_id" not in session:
        return redirect(url_for("vendor.login"))
    
    vendor = VendorObj(session["vendor_id"], db_session)
    vendor.remove_product(product_id)
    
    flash("Product deleted successfully!", "success")
    return redirect(url_for("vendor.dashboard"))

@vendor_bp.route("/track_orders")
def track_orders():
    if "vendor_id" not in session:
        return redirect(url_for("vendor.login"))
    
    vendor = VendorObj(session["vendor_id"], db_session)
    orders = vendor.track_orders()
    return render_template("vendor/orders.html", orders=orders)

@vendor_bp.route("/payouts")
def payouts():
    if "vendor_id" not in session:
        return redirect(url_for("vendor.login"))
    
    vendor = VendorObj(session["vendor_id"], db_session)
    payouts = vendor.manage_payouts()
    return render_template("vendor/payouts.html", payouts=payouts)

@vendor_bp.route("/products")
def vendor_products():
    products = VendorObj(session['vendor_id'] ,
                         db_session=db_session).get_product('vendor_id',
                                                            value=session['vendor_id'] , occurrence='all')
    return render_template("vendor/products.html",products=products)