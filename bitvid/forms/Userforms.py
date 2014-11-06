from flask_wtf import Form
from wtforms import PasswordField, validators

class ChangePassword(Form):
    old_password =  PasswordField('Old Password', [validators.InputRequired()])
    password = PasswordField('New Password', [validators.InputRequired(), validators.EqualTo('confirm', message='Passwords must match')])
    confirm  = PasswordField('Repeat Password', [validators.InputRequired()])

