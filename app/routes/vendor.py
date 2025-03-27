from flask import Blueprint, render_template, request, redirect, url_for, flash, session , jsonify

from app.data_manager.vendor import VendorObj
from config.config import JSONConfig
from app.routes.routes_utils import meet_vendor_requirements , session_set
from app.data_manager.users_manager import UserManager

from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine


config = JSONConfig('config.json')

engine = create_engine(f"sqlite:///{config.database_url.absolute()}")
Session = sessionmaker(bind=engine)
db_session = Session()
vendor_bp = Blueprint("vendor", __name__, url_prefix="/vendor")




@vendor_bp.route("/login")
@session_set
def login():
    session['IS_VENDOR'] = True
    if  'vendor_id' not in session:
        return redirect(url_for("user.login"))
    else:
        return redirect(url_for("vendor.dashboard"))
    
    

@vendor_bp.route("/login/<vendoid>")
@session_set
def login2(vendoid):
    session['vendor_id'] = vendoid
    return redirect(url_for("vendor.dashboard"))


@vendor_bp.route("/logout")
@meet_vendor_requirements
@session_set
def logout():
    session.clear()
    return redirect (url_for("vendor.login"))

@vendor_bp.route("/register")
@session_set
def register():
    session['vendor_register'] = True
    return redirect (url_for('user.register'))
 

@vendor_bp.route("/")
@session_set
def vendorhome():
    return render_template("vendor/home.html")

@vendor_bp.route("/update-details" , methods = ['POST' , "GET"])
@session_set
def add_details():
    name = session.get("user_name" , None)
    if not name:
        return redirect (url_for("vendor.login"))
    
    user_obj = UserManager(db_session=db_session , user=name)
    if request.method == "POST":
        data = request.get_json().get('data')
       
        data['name'] = name
        vendor_ = VendorObj.register_vendor(db_session=db_session ,data=data)
        session['vendor_id'] = vendor_.vendor_id
    if 'vendor_id' in session:
        vendor_ = VendorObj(db_session=db_session , vendor_id=session.get('vendor_id'))
        extra_data = {'name':name , 'email':vendor_.vendor_table.email , 'phone':vendor_.vendor_table.phone , 
                      'store_logo':vendor_.vendor_table.store_logo , 'store_description':vendor_.vendor_table.store_description
                      ,'store_name':vendor_.vendor_table.store_name}
    else:
        extra_data = {'name':user_obj.user.name , 'phone':user_obj.user.phone ,'email':user_obj.user.email}
    return render_template("vendor/update_details.html" , name=name , data=extra_data )
  
@vendor_bp.route("/dashboard")
@meet_vendor_requirements
@session_set
def dashboard():

    vendor = VendorObj(session['vendor_id'], db_session=db_session)

    data =vendor.get_dashboard_data()
    print(data)
    return render_template(
        "vendor/vendor_details2.html",
        data = data
    )


@vendor_bp.route("/add_product", methods=["GET", "POST"])
@meet_vendor_requirements
@session_set
def add_product():
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

        return redirect(url_for("vendor.dashboard"))
    
    return render_template("vendor/add_product.html")


@vendor_bp.route("/product-details/<int:product_id>", methods=["GET", "POST"])
@meet_vendor_requirements
@session_set
def product_details(product_id):
    return "hello"

@vendor_bp.route("/edit_product/<int:product_id>", methods=["GET", "POST"])
@meet_vendor_requirements
@session_set
def edit_product(product_id):
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
        print("here is the data" , updated_data)
        vendor.modify_products([{"id": product_id, "data": updated_data}])
        return jsonify({"success":True}) , 200
    return render_template("vendor/edit_product2.html", product_id=product_id , product=product )

@vendor_bp.route("/delete_product/<int:product_id>", methods=["POST"])
@meet_vendor_requirements
@session_set
def delete_product(product_id):

    
    vendor = VendorObj(session["vendor_id"], db_session)
    vendor.remove_product(product_id)
    
    return redirect(url_for("vendor.dashboard"))



@vendor_bp.route("/track_orders")
@meet_vendor_requirements
@session_set
def track_orders():
    return redirect(url_for("vendor.dashboard"))


@vendor_bp.route("/payouts")
@meet_vendor_requirements
@session_set
def payouts():

    vendor = VendorObj(session["vendor_id"], db_session)
    payouts = vendor.manage_payouts()
    return render_template("vendor/payouts.html", payouts=payouts)

@vendor_bp.route("/products")
@meet_vendor_requirements
@session_set
def vendor_products():
    products = VendorObj(session['vendor_id'] ,
                         db_session=db_session).get_product('vendor_id',
                                                            value=session['vendor_id'] , occurrence='all')
    return render_template("vendor/products.html",products=products)


@vendor_bp.route("/upload" , methods = ['POST'])
@session_set
def upload_image():
    import os 
    from pathlib import Path

    print(request.files)
    if "store_logo_file" not in request.files and "image" not in request.files:
        return jsonify({"success": False, "error": "No file part"}) , 500

    file = request.files.get("store_logo_file") 
    if not file:
        file = request.files.get("image") 
    if not file:
        return jsonify({"success": False, "error": "No file part"}) , 500
    if file.filename == "":
        return jsonify({"success": False, "error": "No selected file"})

    if file:
        filepath = os.path.join("/home/ajay/Documents/VENDOR-PROJECT/app/static/uploads", file.filename)
        Path(filepath).parent.mkdir(parents=True  , exist_ok=True)
        print("saving file in file path" , filepath)
        file.save(filepath)
        image_url = url_for("static", filename=f"uploads/{file.filename}", _external=True)
        return jsonify({"success": True, "image_url": image_url})

    return jsonify({"success": False, "error": "Unknown error"})
