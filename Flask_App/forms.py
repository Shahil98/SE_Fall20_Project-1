from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length


class signupForm(FlaskForm):
    # create a form for login, in this case we just need uid, 
    # Datarequired means we do not accept empty string as input and the length
    # should be 1-200  
    uid = StringField('Uid', validators=[DataRequired(), Length(min=1, max=200)])
    submit = SubmitField('Submit')
