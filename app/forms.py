from flask.ext.wtf import Form
from wtforms import TextField, BooleanField, PasswordField, TextAreaField, SelectField
from wtforms.validators import Required, Length, email, url
import os

class LoginForm(Form):
    email = TextField('email', validators = [Required(), Length(min = 4, max = 50), email])
    password = PasswordField('password', validators = [Required()])
    remember_me = BooleanField('remember_me', default = False)

class AddSessionForm(Form):
	title = TextField('title', validators = [Required(), Length(min = 5, max = 100)])
	description = TextAreaField('description', validators = [Length(min = 0, max = 4000)])

class AddNewsForm(Form):
	title = TextField('title', validators = [Required(), Length(min = 5, max= 100)])
	description = TextAreaField('description', validators = [Length(min = 0, max = 4000)])
	