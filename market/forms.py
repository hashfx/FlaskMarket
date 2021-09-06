from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, HiddenField
from wtforms.validators import Length, EqualTo, Email, DataRequired, ValidationError
from market.models import User


class RegisterForm(FlaskForm):

    # verify that a user is unique
    def validate_username(self, username_to_check):
        """ validation to check if username already exists """
        user = User.query.filter_by(username=username_to_check.data).first()  # check if database has existing username
        if user:  # if var user is not None
            raise ValidationError('Username already exists! Try a different Username')

    def validate_email(self, email_to_check):
        email = User.query.filter_by(email_address=email_to_check.data).first()  # check if database has existing email
        if email:
            raise ValidationError('Email Address already exists! Try a different Email')

    # labels for form
    username = StringField(label='User Name: ', validators=[Length(min=2, max=30), DataRequired()])
    email = StringField(label='Email: ', validators=[Email(), DataRequired()])
    password1 = PasswordField(label='Password: ', validators=[Length(min=6), DataRequired()])
    password2 = PasswordField(label='Confirm Password: ', validators=[EqualTo('password1'), DataRequired()])
    submit = SubmitField(label='Create Account')


class LoginForm(FlaskForm):
    username = StringField(label='User Name: ', validators=[DataRequired()])
    password = PasswordField(label='Password: ', validators=[DataRequired()])
    submit = SubmitField(label='Sign In')


class PurchaseItemForm(FlaskForm):
    submit = SubmitField(label='Purchase Item!')


class SellItemForm(FlaskForm):
    submit = SubmitField(label='Sell Item!')
