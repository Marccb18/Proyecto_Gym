from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from models import Usuario

app = Flask(__name__)
app.config.from_object("config")

db = SQLAlchemy(app)
login_manager = LoginManager(app)


@app.route("/")
def inicio():
    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)
