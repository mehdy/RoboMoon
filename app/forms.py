from flask.ext.wtf import Form
from wtforms import TextField, BooleanField, PasswordField, TextAreaField, SelectField
from wtforms.validators import Required, Length, email, url
import os

class LoginForm(Form):
    email = TextField('email', validators = [Required(), Length(min = 4, max = 100), email])
    password = PasswordField('password', validators = [Required()])
    remember_me = BooleanField('remember_me', default = False)

class AddSessionForm(Form):
	title = TextField('title', validators = [Required(), Length(min = 5, max = 100)])
	description = TextAreaField('description', validators = [Length(max = 4000)])

class AddNewsForm(Form):
	title = TextField('title', validators = [Required(), Length(min = 5, max= 100)])
	description = TextAreaField('description', validators = [Length(max = 4000)])
	
class EditProfileForm(Form):
	username = TextField('username', validators = [Required(), Length(max = 50)])
	password = PasswordField('password', validators = [Required(), Length(min =8, max = 64)])
	confirm = PasswordField('confirm', validators = [Required(), Length(min =8, max = 64)])
	email = TextField('email', validators = [Required(), Length(min = 4, max = 100), email])
	website = TextField('website', validators = [Length(max = 50)])
	bio = description = TextAreaField('bio', validators = [Length(max = 256)])

class AddUserForm(Form):
	username = TextField('username', validators = [Required(), Length(max = 50)])
	password = PasswordField('password', validators = [Required(), Length(min =8, max = 64)])
	confirm = PasswordField('confirm', validators = [Required(), Length(min =8, max = 64)])
	email = TextField('email', validators = [Required(), Length(min = 4, max = 100), email])