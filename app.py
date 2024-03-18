from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from models import Usuario

app = Flask(__name__)

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
def index():
    return render_template("index.html")


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
