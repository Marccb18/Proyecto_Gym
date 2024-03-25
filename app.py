from flask import Flask, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import (
    LoginManager,
    UserMixin,
    login_user,
    logout_user,
    login_required,
    current_user,
)
from forms import RegistroForm, LoginForm

app = Flask(__name__)
app.secret_key = "1234"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///gym.db"
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "index"


class User(UserMixin, db.Model):
    id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("index"))
    signup_form = RegistroForm()
    if signup_form.validate_on_submit():
        try:
            username = signup_form.usuario.data
            email = signup_form.email.data
            password = signup_form.password.data
            hashed_password = generate_password_hash(password)
            new_user = User(username=username, email=email, password=hashed_password)
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=False)
            return redirect(url_for("index"))
        except:
            return render_template("signup_form.html", form=signup_form, error=True)

    return render_template("signup_form.html", form=signup_form, error=False)


@app.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("index"))
    login_form = LoginForm()
    if login_form.validate_on_submit():
        email = login_form.email.data
        password = login_form.password.data

        user = User.query.filter_by(email=email).first()

        if user and check_password_hash(user.password, password):
            login_user(user, remember=False)
            return redirect(url_for("index"))
        else:
            return render_template("login_form.html", form=login_form, error=True)

    return render_template("login_form.html", form=login_form, error=False)


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("index"))


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
