from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import Length, EqualTo, Email


class RegisterForm(FlaskForm):
    username = StringField(label='User Name:', validators=Length(min=3, max=100))
    email_address = StringField(label='Email Address:', validators=Email())
    password1 = PasswordField(label='Password:', validators=Length(min=3))
    password2 = PasswordField(label='Confirm Password:', validators=EqualTo('password1'))
    submit = SubmitField(label='Create Account')
