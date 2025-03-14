from flask import Blueprint, render_template, request, redirect, url_for, session, flash, g

from app.models.user_profile import UserProfile as User 

from config.config import JSONConfig

from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

config = JSONConfig('config.json')

engine = create_engine(f"sqlite:///{config.database_url.absolute()}")
Session = sessionmaker(bind=engine)
db_session = Session()

user_bp = Blueprint("user", __name__, url_prefix="/user")

@user_bp.before_request
def load_current_user():
    """Loads the logged-in user for all user routes"""
    user_id = session.get("user_id")
    if user_id:
        g.current_user = db_session.query(User).filter_by(id=user_id).first()
    else:
        g.current_user = None

@user_bp.route("/login", methods=["GET", "POST"])
def login():
    """User login"""
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]  # Hash-checking needed
        user = db_session.query(User).filter_by(email=email).first()

        if user and user.check_password(password):  # Assuming you have a password check function
            session["user_id"] = user.id
            flash("Login successful", "success")
            return redirect(url_for("shop.shop_home"))
        else:
            flash("Invalid credentials", "danger")

    return render_template("user/login.html")

@user_bp.route("/register", methods=["GET", "POST"])
def register():
    """User registration"""
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        user = User(email=email)
        user.set_password(password)  # Assuming you have a password setter method

        db_session.add(user)
        db_session.commit()

        session["user_id"] = user.id  # Auto-login after register
        flash("Registration successful", "success")
        return redirect(url_for("shop.shop_home"))

    return render_template("user/register.html")

@user_bp.route("/logout")
def logout():
    """Logs out the user"""
    session.pop("user_id", None)
    flash("Logged out successfully", "info")
    return redirect(url_for("shop.shop_home"))

@user_bp.route("/profile")
def profile():
    """User profile page"""
    if not g.current_user:
        return redirect(url_for("user.login"))
    return render_template("user/profile.html", user=g.current_user)

@user_bp.route("/orders")
def orders():
    """User order history"""
    if not g.current_user:
        return redirect(url_for("user.login"))
    
    orders = g.current_user.orders  # Assuming you have a relationship setup
    return render_template("user/orders.html", orders=orders)
