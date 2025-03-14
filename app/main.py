# main.py
from flask import Flask , session , request , jsonify
from app.routes.vendor import vendor_bp
from app.routes.shop import shop_bp

from app.routes.user import user_bp


app = Flask(__name__ ,static_folder= "/home/ajay/Documents/VENDOR-PROJECT/app/static")
app.secret_key = "djk"
app.register_blueprint(vendor_bp)
app.register_blueprint(shop_bp)
app.register_blueprint(user_bp)




if __name__ == "__main__":
    app.run(debug=True)
