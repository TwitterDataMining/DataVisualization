from flask_wtf import FlaskForm
from wtforms import TextAreaField, PasswordField


class LoginForm(FlaskForm):
    username = TextAreaField('username')
    password = PasswordField('password')




