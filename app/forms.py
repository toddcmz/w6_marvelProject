from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField, SelectMultipleField
from wtforms.validators import DataRequired, Email
from app import heroChoices

class SignupForm(FlaskForm):
    username = StringField('username', validators=[DataRequired()])
    first_name = StringField('first_name', validators =[DataRequired()])
    last_name = StringField('last_name', validators =[DataRequired()])
    email = StringField('email', validators=[DataRequired(), Email()])
    password = PasswordField('password', validators=[DataRequired()])
    submit = SubmitField('Sign Up')

class SigninForm(FlaskForm):
    username = StringField('username', validators=[DataRequired()])
    password = PasswordField('password', validators=[DataRequired()])
    submit = SubmitField('Sign In')

class AssembleForm(FlaskForm):
    teamName = StringField('Team Name', validators=[DataRequired()])
    avenger1 = SelectField('Pick first avenger', choices=heroChoices)
    avenger2 = SelectField('Pick second avenger', choices=heroChoices)
    avenger3 = SelectField('Pick third avenger', choices=heroChoices)
    submit = SubmitField('Create Team')

class CodexForm(FlaskForm):
    heroName = SelectField('Pick an avenger', choices=heroChoices)
    submit = SubmitField('View Details')