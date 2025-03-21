# main.py
from flask import Flask , session
from app.routes.vendor import vendor_bp
from app.routes.shop import shop_bp
from app.routes.user import user_bp
from app.routes.info import info_bp





app = Flask(__name__ ,static_folder= "/home/ajay/Documents/VENDOR-PROJECT/app/static")
app.secret_key = "djk"

app.register_blueprint(vendor_bp)
app.register_blueprint(shop_bp)
app.register_blueprint(user_bp)
app.register_blueprint(info_bp)


@app.route("/log")
def log_out():
    session.clear()
    return "Bye"

@app.route("/")
def g():
    return "".join([f"<br> {k}: {v}</br>" for k,v in session.items()])

if __name__ == "__main__":
    app.run(debug=True)
