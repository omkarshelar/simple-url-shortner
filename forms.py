from flask_wtf import FlaskForm
from wtforms import validators, StringField, SubmitField, PasswordField

class ShortenForm(FlaskForm):
	link = StringField("Link : ", [validators.DataRequired()])
	short_link = StringField("Custom Short Link (Optional) : ",[validators.Length(max=10,message="Length of short link must be between 5 and 10 characters")])
	submit = SubmitField('Shorten!')

class SignupForm(FlaskForm):
	name = StringField("Username:", [validators.DataRequired()])
	password = PasswordField("Password", [validators.DataRequired()])
	password_conf = PasswordField("Confirm Password", [validators.DataRequired()])
	submit = SubmitField('Signup!')

class LoginForm(FlaskForm):
	name = StringField("Username:", [validators.DataRequired()])
	password = PasswordField("Password", [validators.DataRequired()])
	submit = SubmitField('Login!')
