from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()], id='username')
    password = PasswordField('Password', validators=[DataRequired()], id='password')
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In', id='submit')