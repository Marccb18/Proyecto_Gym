from flask import Flask, render_template, request, flash, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, EqualTo
from forms import RegistroForm
from models import Usuario


app = Flask(__name__)

app.config["SECRET_KEY"] = "tu_clave_secreta_aqui"

# Configuración de la base de datos
app.config["SQLALCHEMY_DATABASE_URI"] = (
    "sqlite:///gym.db"  # Cambia esto según tu configuración
)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Inicializa la extensión SQLAlchemy
db = SQLAlchemy(app)

login_manager = LoginManager(app)


# Asigna la vista de login requerida
login_manager.login_view = "iniciar"

# Inicializa la extensión LoginManager
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    return Usuario.query.get(int(user_id))


@app.route("/")
def inicio():
    return render_template("index.html")


@app.route("/iniciar")
def iniciar():
    return render_template("login_form.html")


@app.route("/registrar", methods=["POST", "GET"])
def registrar():
    form = RegistroForm()  # Crear una instancia del formulario
    if request.method == "POST":
        # Obtiene los datos del formulario
        usuario = request.form.get("usuario")
        password = request.form.get("password")

        # Corroborar si existe el usuario
        existe_usuario = Usuario.query.filter_by(usuario=usuario).first()

        if existe_usuario:
            flash("El usuario ya existe.")
            return redirect(url_for("registrar"))

        # Crea un nuevo ususario
        nuevo_usuario = Usuario(usuario=usuario)
        nuevo_usuario.set_password(password)

        # Guardar usuario en la base de datos
        db.session.add(nuevo_usuario)
        db.session.commit()

        flash("Se creó el nuevo usuario")
        return redirect(url_for(iniciar))

    return render_template("signup_form.html", form=form)


@app.route("/cerrar")
def cerrar():
    return render_template("cerrar.html")


@app.route("/perfil")
def perfil():
    return render_template("perfil.html")


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
