from flask import Flask, render_template, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import (
    LoginManager,
    current_user,
    login_user,
    logout_user,
    login_required,
)
from app.models import User
from app.forms import LoginForm, RegistrationForm

app = Flask(__name__)
app.config.from_object("config")

db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)


@app.route("/")
def index():
    return render_template("index.html")
