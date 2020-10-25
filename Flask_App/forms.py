from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length


class signupForm(FlaskForm):

    uid = StringField('Uid', validators=[DataRequired(), Length(min=1, max=200)])
    submit = SubmitField('Submit')
