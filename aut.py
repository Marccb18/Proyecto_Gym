from flask import (
    Blueprint,
    render_template,
    request,
    url_for,
    redirect,
    flash,
    session,
    g,
)


from werkzeug.security import generate_password_hash, check_password_hash
from .models import User
from ToDo import db

bp = Blueprint("aut", __name__, url_prefix="/aut")


@bp.route("/registro", methods=["GET", "POST"])
def registro():
    if request.method == "POST":
        username = request.form["username"]
        email = request.form["email"]
        password = request.form["password"]

        usuario = User(username, email, generate_password_hash(password))

        error = None

        nombre_usuario = User.query.filter_by(username=username).first()

        if nombre_usuario == None:
            db.session.add(usuario)
            db.session.commit()

            return redirect(url_for("aut.acceder"))
        else:
            error = f"El usuario {username} ya existe, ingrese otro nombre de usuario"
            flash(error)

    return render_template("aut/registro.html")


@bp.route("/acceder", methods=["GET", "POST"])
def acceder():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        error = None
        # validar datos

        usuario = User.query.filter_by(username=username).first()

        if usuario == None:
            error = "No existe ese usuario"
        elif not check_password_hash(usuario.password, password):
            error = "El password es incorrecto"

        if error is None:
            session.clear()
            session["usuario_id"] = usuario.id

            return redirect(url_for("app.lista"))

        flash(error)
    return render_template("aut/acceder.html")


@bp.before_app_request
def load_logged_in_user():
    usuario_id = session.get("usuario_id")
    if usuario_id is None:
        g.usuario = None
    else:
        g.usuario = User.query.get_or_404(usuario_id)


@bp.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("index"))


import functools


def login_required(vista):
    @functools.wraps(vista)
    def capturando_vista(**kwargs):
        if g.usuario is None:
            return redirect(url_for("aut.acceder"))
        return vista(**kwargs)

    return capturando_vista
