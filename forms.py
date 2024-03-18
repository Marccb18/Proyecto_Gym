from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, EqualTo


class RegistroForm(FlaskForm):
    usuario = StringField("Usuario", validators=[DataRequired(), Length(min=4, max=32)])
    password = PasswordField("Contraseña", validators=[DataRequired(), Length(min=8)])
    confirmar_password = PasswordField(
        "Confirmar Contraseña", validators=[DataRequired(), EqualTo("password")]
    )
    submit = SubmitField("Registrarse")
