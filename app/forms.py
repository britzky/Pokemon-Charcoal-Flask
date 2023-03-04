from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, EmailField, PasswordField
from wtforms.validators import DataRequired, EqualTo

# Forms Section
class PokemonForm(FlaskForm):
    name = StringField('Enter Pokemon: ', validators=[DataRequired()]) 
    submit_btn = SubmitField('Submit')

class SignUpForm(FlaskForm):
    first_name = StringField('First Name: ', validators=[DataRequired()])
    last_name = StringField('Last Name: ', validators=[DataRequired()])
    email = EmailField('Email: ', validators=[DataRequired()])
    password = PasswordField('Password: ', validators=[DataRequired()])
    confirm = PasswordField('Confirm Password: ', validators=[DataRequired(), EqualTo('confirm')]) 
    submit_btn = SubmitField('Submit')
class LoginForm(FlaskForm):
    email = EmailField('Email: ', validators=[DataRequired()])
    password = PasswordField('Password: ', validators=[DataRequired()])
    submit_btn = SubmitField('Submit')