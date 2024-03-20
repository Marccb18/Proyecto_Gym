from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy

class Usuario(UserMixin, db.Model):
    def __init__(self,db):
        self.id = db.Column(db.Integer(10), primary_key=True)
        self.username = db.Column(db.String(64), index=True, unique=True)
        self.password_hash = db.Column(db.String(128))

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f"<Usuario {self.username}>"
