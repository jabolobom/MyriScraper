from flask_wtf import FlaskForm
from wtforms import *

class sourcesForm(FlaskForm):
    source = SelectField(u'Source', choices=[('PSX', 'PSX'),('PS2', 'PS2'),('N64', 'N64')]) # add new sources here
