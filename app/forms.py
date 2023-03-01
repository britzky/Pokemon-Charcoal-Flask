from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

# Forms Section
class PokemonForm(FlaskForm):
    name = StringField('Enter Pokemon: ', validators=[DataRequired()]) 
    submit_btn = SubmitField('Submit')

