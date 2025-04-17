from flask import Blueprint, render_template, request, redirect, url_for, session , jsonify ,g
import os
from pathlib import Path
from app.data_manager.vendor import VendorObj
from config.config import JSONConfig
from app.routes.routes_utils import meet_vendor_requirements , session_set
from app.data_manager.users_manager import UserManager

from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from datetime import datetime
from app.routes.logger import LOG , bp_error_logger
from app.services.upload import ImageManager
from app.models.model_utils import WithDrawAvlailableMethods ,PaymentMethod
from config.envrion_variables import StatusCodes


config = JSONConfig('config.json')

engine = create_engine(f"sqlite:///{config.database_url.absolute()}")
Session = sessionmaker(bind=engine)
db_session = Session()
vendor_bp = Blueprint("vendor", __name__, url_prefix="/vendor")





@vendor_bp.before_request
def load_current_user():
    user_id = session.get('vendor_id')
    if user_id:
        g.current_user = VendorObj(session.get('vendor_id') ,db_session).vendor_table
        if not g.current_user:
            session.clear()
        else:
            g.current_user.is_authenticated = True
    else:
        g.current_user = None

@vendor_bp.context_processor
def inject_user():
   
    user = getattr(g, 'current_user', None)
    return {
        'current_user': user,
        'is_authenticated': user is not None,
        'now': datetime.now()
    }

@vendor_bp.route("/temp")
def test_base():
    return render_template("vendor/base2.html")

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
    data =vendor.get_dashboard_data(stock_threshold=7)

    return render_template(
        "vendor/dashboard2.html",
        data = data
    )


@vendor_bp.route("/add_product", methods=["GET", "POST"])
@meet_vendor_requirements
@session_set
def add_product():
    categories = VendorObj.get_vendor_product_categories(db_session , session.get("vendor_id"))
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

    return render_template("vendor/add_product.html",categories=categories)


@vendor_bp.route("/product-details/<int:product_id>", methods=["GET", "POST"])
@meet_vendor_requirements
@session_set
def product_details(product_id):
    return edit_product(product_id)

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
        vendor.modify_products([{"id": product_id, "data": updated_data}])
    return render_template("vendor/edit_product.html", product_id=product_id , product=product)


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



@vendor_bp.route("/products")
@meet_vendor_requirements
@session_set
def vendor_products():
    products = VendorObj(session['vendor_id'] ,
                         db_session=db_session).get_product('vendor_id',
                                                            value=session['vendor_id'] , occurrence='all')
    categories = VendorObj.get_vendor_product_categories(db_session , session.get("vendor_id"))
    print(categories)
    return render_template("vendor/products.html",products=products , categories=categories)




methods = ["POST", "GET"] if os.getenv("CUSTOM_DEBUG_MODE", "").lower() in ("true", "1", "yes")  else ["POST"]
@vendor_bp.route('/upload', methods=methods)
@meet_vendor_requirements
@session_set
def upload_image():

    
    if request.method == 'GET':
        return render_template("upload.html")

    file = request.files.get('image') or request.files.get('store_logo_file')
    ImageManager._validate_file(file)
    pre_uploaded_image  = ImageManager.validate_image_not_duplicate(db_session=db_session,
                                                                   name=file.filename)
    if pre_uploaded_image:
        LOG.VENDOR_LOGGER.info(f"[IMAGE UPLOAD] duplication detected {pre_uploaded_image.__repr__()}")
        return jsonify({
            "success": True,
            "image_url": pre_uploaded_image.imageurl,
            "public_id": pre_uploaded_image.uniqueid
        }), 200 

    upload_dir = Path(ImageManager.config.TEMP_UPLOAD_IMAGE_DIR)
    local_path = upload_dir/file.filename
    file.save(local_path)
    
    image_url = url_for("static", filename=f"uploads/temp/{file.filename}", _external=True)
    
    public_id = ImageManager.generate_public_id(file.filename)
    cloudinary_url = ImageManager.upload_and_transform_image(
        image_path=local_path,
        public_id=public_id,
        size_idx=2
    )

    LOG.VENDOR_LOGGER.info(f"[IMAGE UPLOAD] {session.get('vendor_id')} uploaded an image {image_url}: cloudinary url {cloudinary_url}")
    if not cloudinary_url:
        ImageManager.save_local_image_url(image_path=Path(local_path),image_url =image_url)
        cloudinary_url = image_url
    else:
        os.remove(local_path)

    ImageManager.record_image_upload(
        db_session=db_session,
        image_url=cloudinary_url,
        public_id=public_id,
        vendor_id=session['vendor_id'],
        filename=file.filename
    )

    return jsonify({
        "success": True,
        "image_url": cloudinary_url,
        "public_id": public_id
    }), 200


# ==================
# to be worked on ||
# ==================

@vendor_bp.route("/orders")
@meet_vendor_requirements
@session_set
def orders():
    return "order in view"


@vendor_bp.route("/payouts", methods=['GET', 'POST'])
@meet_vendor_requirements
@session_set
def payouts():
    vendor = VendorObj(session["vendor_id"], db_session)
    vendor_balance, withdrawals = vendor.manage_payouts()
    
    # Prepare data for both HTML and JSON responses
    withdrawals_data = [{
        'amount': float(w['amount']),
        'method': w['method'].value,
        'request': w['request'].isoformat(),
        'status': w['status']
    } for w in withdrawals]
    
    if request.method == "POST" :
        return jsonify({
            'withdrawals': withdrawals_data,
            'balance': {
                'available': float(vendor_balance['available']),
                'pending': float(vendor_balance['pending']),
                'total': float(vendor_balance['total'])
            }
        })
    
    return render_template("vendor/payouts.html",
                        vendor_balance=vendor_balance,
                        withdrawals=withdrawals,
                        payment_methods=list(WithDrawAvlailableMethods),
                        default_account_number=vendor.vendor_table.phone)



@vendor_bp.route("/reports")
def reports():
    return "helo reports"



@vendor_bp.route("/process-pay" , methods = ['POST'])
@meet_vendor_requirements
@session_set
@bp_error_logger(LOG.VENDOR_LOGGER , status_code=400)
def process_withdrawal():
 
    form_data = request.form
    amount =float(form_data.get("amount"))
    method = form_data.get('method')
    account_info = form_data.get('account_info')


    if account_info.startswith("07"):
        account_info = "254" + account_info[1:]

    if not all((amount,method,account_info)) :
        raise ValueError("missing values from {} {} {}".format(amount,method,account_info))
    
    enum_instance = PaymentMethod[method]

    vendor = VendorObj(session['vendor_id'], db_session)

    verified_to_withdraw = vendor.is_allowed_withdraw(db_session=db_session,vendor_id=session['vendor_id'] ,needed_amount=amount)

    if not "success" in verified_to_withdraw :
        return jsonify(verified_to_withdraw), 400

    if not verified_to_withdraw:
        return jsonify({"message":"You are not allowed to withdraw funds"}), 400
    

    response ,request_successful = vendor.withdraw(amount,account_info)

    LOG.VENDOR_LOGGER.info("[WITHDRAWAL] response from payment gateway: {}".format(response))

    if not response:
        return jsonify({
            "message":"error proccessing request",
            "data":"Try again later"}) , 400

    if not request_successful:
        return jsonify({
            "status": "error",
            "message": response['message']
        }), 400



    vendor.create_vendor_payout_record(
        db_session=db_session,
        vendor_id=session['vendor_id'],
        payment_method=enum_instance,
        amount=amount,
        batch_id=response['tracking_id'],
        tracking_id=response['reference_ids'][0]
    )

    return jsonify(
        {"message": "success",
         'withdraw_id':response['reference_ids'][0]}
    ) ,200


@vendor_bp.route("/withdrawal-status/<withdraw_id>")
@meet_vendor_requirements
@session_set
@bp_error_logger(LOG.VENDOR_LOGGER , status_code=400)
def check_withdrawal_status(withdraw_id):
    

    if not withdraw_id:
        return jsonify({"message":"missing withdraw id"}), 400
    
    response =  VendorObj.check_update_withdraw_status(db_session ,withdraw_id)
    response = response['data'][0]

    LOG.VENDOR_LOGGER.debug("[WITHDRAWAL] response from payment gateway: {}".format(response))
    status = "pending"
    if response['status_code'] in StatusCodes.SUCCESS:
        status = 'completed'
        message = "Withdrawal successfull"

    elif response['status_code'] in StatusCodes.CANCELED:
        message = "Withdrawal canceled"

    elif response['status_code'] in StatusCodes.WAITING:
        message = "Withdrawal is pending"

    elif response['status_code'] in StatusCodes.CONTACT_ADMIN:
        message = "Contact admin"

    elif response['status_code'] == "error":
        message = "Error processing request"
        return jsonify({
            "message":message,
            "status":'error',
        }), 400
    
    else:
        message = "With draw is pending"
    
    return jsonify({
            "message":message,
            "data":"None",
            "status":status,
        }) , 200


@vendor_bp.route("/pending-withdraws" ,methods = ['POST'])
@meet_vendor_requirements
def get_pending_withdrawals():
    
    vendor_id = int(session['vendor_id'])
    pending_ids = VendorObj.get_pending_withdrawals(vendor_id = vendor_id , db_session=db_session)
    pending_data = {"message":"success","ids":pending_ids if pending_ids else []}
 
    return jsonify(pending_data) ,200



@vendor_bp.route("/withdrawal-history-pay")
def withdrawal_history():
    return jsonify({"sussess":True})

