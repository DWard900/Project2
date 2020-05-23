from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField, SelectField, IntegerField, TimeField, FloatField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, Length, NumberRange
from app.models import User
from wtforms.fields.html5 import DateField

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')

class EditProfileForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    about_me = TextAreaField('About me', validators=[Length(min=0, max=140)])
    submit = SubmitField('Submit')

class SetGoal(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    goals = TextAreaField('Goals', validators=[Length(min=0, max=500)])
    submit = SubmitField('Submit')

class ExerciseForm(FlaskForm):
    styles = [('Walk','Walk'), ('Run','Run')] #Not sure why this need to be a tuple rather than just a single string?
    rating = [('1','1'),('2','2'),('3','3'),('4','4'),('5','5'),('6','6'),('7','7'),('8','8'),('9','9'),('10','10'),]
    style = SelectField('Enter type of exercise', choices= styles, validators=[DataRequired()])
    distance = FloatField('Enter distance of exercise', validators=[DataRequired()], render_kw={"placeholder": "Distance in KM"})
    time = FloatField('Enter time', render_kw={"placeholder": "Time in mintues"})
    date = DateField()
    rate_exercise = SelectField('How did you feel during your exercise', choices= rating, default=10 )
    exercise_comments = StringField('Comments', render_kw={"placeholder": "I felt this exercise was ...."})
    submit = SubmitField('Submit')

class EmptyForm(FlaskForm):
    submit = SubmitField('Submit')

class MessageForm(FlaskForm):
    message = TextAreaField(('Message'), validators=[
        DataRequired(), Length(min=0, max=140)])
    
    submit = SubmitField(('Submit'))