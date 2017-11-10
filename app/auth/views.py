# app/auth/views.py

from flask import flash, redirect, render_template, url_for, request, current_app
from flask_login import login_required, login_user, logout_user

from . import auth
from forms import LoginForm, RegistrationForm,ResetPassword, ResetPasswordSubmit
from .. import db
from email import send_email

from ..models import Employee
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer,URLSafeTimedSerializer
from flask_mail import Message


@auth.route('/register', methods=['GET', 'POST'])
def register():
    """
    Handle requests to the /register route
    Add an employee to the database through the registration form
    """
    form = RegistrationForm()
    if form.validate_on_submit():
        employee = Employee(email=form.email.data,
                            username=form.username.data,
                            first_name=form.first_name.data,
                            last_name=form.last_name.data,
                            department = form.department.data,
                            role = form.role.data,
                            password=form.password.data)

        # add employee to the database
        db.session.add(employee)
        db.session.commit()
        flash('You have successfully registered! You may now login.')

        # redirect to the login page
        return redirect(url_for('auth.login'))

    # load registration template
    return render_template('auth/register.html', form=form, title='Register')


@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():

        # check whether employee exists in the database and whether
        # the password entered matches the password in the database
        employee = Employee.query.filter_by(email=form.email.data).first()
        if employee is not None and employee.verify_password(
                form.password.data):
            # log employee in
            login_user(employee)

            # redirect to the appropriate dashboard page
            if employee.is_admin:
                return redirect(url_for('home.admin_dashboard'))
            else:
                return redirect(url_for('home.dashboard'))

        # when login details are incorrect
        else:
            flash('Invalid email or password.')

    # load login template
    return render_template('auth/login.html', form=form, title='Login')

    
@auth.route('/logout')
@login_required
def logout():
    """
    Handle requests to the /logout route
    Log an employee out through the logout link
    """
    logout_user()
    flash('You have successfully been logged out.')

    # redirect to the login page
    return redirect(url_for('auth.login'))


# @auth.route('/reset-password', methods=('GET', 'POST',))
# def forgot_password():
#     token = request.args.get('token',None)
#     form = ResetPassword(request.form) #form
#     if form.validate_on_submit():
#         email = form.email.data
#         user = Employee.query.filter_by(email=email).first()
#         if user:
#             token = user.get_token()
#             # print token
#             verified_result = user.verify_token(token)
#             print('==============')
#             print(verified_result)
#             print('==============')
#             print (token)

#     return render_template('auth/reset.html', form=form)



def send_password_reset_email(user_email):
    password_reset_serializer = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
 
    password_reset_url = url_for(
        'auth.reset_with_token',
        token = password_reset_serializer.dumps(user_email, salt='password-reset-salt'),
        _external=True)
 
    html = render_template(
        'auth/email_password_reset.html',
        password_reset_url=password_reset_url)
 
    send_email(user_email, password_reset_url)


@auth.route('/reset', methods=["GET", "POST"])
def reset():
    form = ResetPassword()
    if form.validate_on_submit():
        try:
            user = Employee.query.filter_by(email=form.email.data).first_or_404()
        except:
            flash('Invalid email address!', 'error')
            return render_template('auth/reset.html', form=form)
         
        # if user.email_confirmed:
        send_password_reset_email(user.email)
        flash('Please check your email for a password reset link.', 'success')
        # else:
        #     flash('Your email address must be confirmed before attempting a password reset.', 'error')
        return redirect(url_for('auth.login'))
 
    return render_template('auth/reset.html', form=form)


@auth.route('/reset/<token>', methods=["GET", "POST"])
def reset_with_token(token):
    try:
        password_reset_serializer = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
        email = password_reset_serializer.loads(token, salt='password-reset-salt', max_age=3600)
    except:
        flash('The password reset link is invalid or has expired.', 'error')
        return redirect(url_for('auth.login'))
 
    form = ResetPasswordSubmit()
 
    if form.validate_on_submit():
        try:
            user = Employee.query.filter_by(email=email).first_or_404()
        except:
            flash('Invalid email address!', 'error')
            return redirect(url_for('users.login'))
 
        user.password = form.password.data
        db.session.add(user)
        db.session.commit()
        flash('Your password has been updated!', 'success')
        return redirect(url_for('auth.login'))
 
    return render_template('auth/reset_password_with_token.html', form=form, token=token)

