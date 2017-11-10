# app/auth/forms.py

from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, SubmitField, ValidationError,TextField
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from wtforms.validators import DataRequired, Email, EqualTo, Required

from ..models import Employee,Role, Department

class RegistrationForm(FlaskForm):
    """
    Form for users to create new account
    """
    email = StringField('Email', validators=[DataRequired(), Email()])
    username = StringField('Username', validators=[DataRequired()])
    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])
    department = QuerySelectField(query_factory=lambda: Department.query.all(),
                                  get_label="name",
                                  allow_blank=True)
    role = QuerySelectField(query_factory=lambda: Role.query.all(),
                            get_label="name",
                            allow_blank=True) 
    password = PasswordField('Password', validators=[
                                        DataRequired(),
                                        EqualTo('confirm_password')
                                        ])
    confirm_password = PasswordField('Confirm Password')
    submit = SubmitField('Register')

    def validate_email(self, field):
        if Employee.query.filter_by(email=field.data).first():
            raise ValidationError('Email is already in use.')

    def validate_username(self, field):
        if Employee.query.filter_by(username=field.data).first():
            raise ValidationError('Username is already in use.')

class LoginForm(FlaskForm):
    """
    Form for users to login
    """
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class ExistingUser(object):
    def __init__(self, message="Email doesn't exists"):
        self.message = message

    def __call__(self, form, field):
        if not Employee.query.filter_by(email=field.data).first():
            raise ValidationError(self.message)

reset_rules = [Required(),
              Email(),
              ExistingUser(message='Email address is not available')]

class ResetPassword(FlaskForm):
    email = TextField('Email', validators=reset_rules)
    submit = SubmitField('Send reset link to email')

class ResetPasswordSubmit(FlaskForm):
    password = PasswordField('Password', 
                            validators=[DataRequired(),
                                        EqualTo('confirm')])
    confirm = PasswordField('Confirm Password')
    submit = SubmitField('Update')