# main.py
from flask import Flask , session
from app.routes.vendor import vendor_bp
from app.routes.shop import shop_bp
from app.routes.user import user_bp
from app.routes.info import info_bp
from pathlib import Path




app = Flask(__name__ ,static_folder= str(Path().cwd()/"app/static"))
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

