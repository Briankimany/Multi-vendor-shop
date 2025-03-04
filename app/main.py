# main.py
from flask import Flask , session
from app.routes.vendor import vendor_bp
from app.routes.shop import shop_bp


app = Flask(__name__)
app.secret_key = "djk"
app.register_blueprint(vendor_bp)
app.register_blueprint(shop_bp)


if __name__ == "__main__":
    app.run(debug=True)
