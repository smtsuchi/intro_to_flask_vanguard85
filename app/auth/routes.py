from flask import Blueprint, render_template, redirect, request, url_for, flash
# import forms and models
from .forms import LoginForm, UserCreationForm
from app.models import User
from werkzeug.security import check_password_hash
from flask_login import login_user, logout_user, login_required, current_user

# import automated mail dependecies
from flask_mail import Message, Mail
mail = Mail()

auth = Blueprint('auth', __name__, template_folder='auth_templates')

from app.models import db

@auth.route('/login', methods=["GET", "POST"])
def logMeIn():
    form = LoginForm()
    if current_user.is_authenticated:
        return redirect(url_for('home'))

    if request.method == "POST":
        if form.validate():
            username = form.username.data
            password = form.password.data
            remember_me = form.remember_me.data

            # check if user exists
            user = User.query.filter_by(username=username).first()

            if user:
                if check_password_hash(user.password, password):
                    login_user(user, remember=remember_me)
                    flash(f'Welcome back, {username}!', 'success')
                    return redirect(url_for('home'))
                else:
                    flash(f'Incorrect password. Please try again.', 'danger')
            else:
                flash(f'No valid user with that username. Please try again.', 'danger')
            return redirect(url_for('auth.logMeIn'))
    return render_template('login.html', form = form)

@auth.route('/signup', methods=["GET", "POST"])
def signMeUp():
    form = UserCreationForm()
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    if request.method == "POST":
        if form.validate():
            username = form.username.data
            email = form.email.data
            password = form.password.data

            # check if user exists
            user = User.query.filter_by(username=username).first()
            if user:
                flash(f'That username already exists. Please pick another name', 'danger')
                return redirect(url_for('auth.signMeUp'))
            # create an instance of our user
            user = User(username, email, password)

            # add instance to database
            db.session.add(user)
            # commit to databse
            db.session.commit()

            msg = Message(
                f"Welcome to Shoha's Bike Shop!",
                body= 'Thank you for joining our mailing list. We sell only the biest bikes. Stay tuned for more deals and fire cops.',
                recipients=[email]
            )

            mail.send(msg)




            flash(f'You have successfully created a new user. Welcome, {username}!', 'success')
            return redirect(url_for('auth.logMeIn'))
        else:
            for key in form.errors:
                if key == 'email':
                    flash(form.errors[key][0], 'danger')
                elif key == 'confirm_password':
                    flash("Your passwords did not match. Please try again", 'danger')
    return render_template('signup.html', form=form)

@auth.route('/logout')
@login_required
def logMeOut():
    logout_user()
    return redirect(url_for('auth.logMeIn'))





# 
# 
#  API ROUTES
# 
# 
@auth.route('/api/signup', methods=["POST"])
def apiSignMeUp():
    data = request.json  
        
    username = data['username']
    email = data['email']
    password1 = data['password1']
    password2 = data['password2']

    if password1 != password2:
        return {
            'status': 'not ok',
            'message': 'The passwords do not match. Try again.'
        }

    # check if user exists
    user = User.query.filter_by(username=username).first()
    if user:
        return {
            'status': 'not ok',
            'message': 'A user with that username already exists. Tough.'
        }
    # create an instance of our user
    user = User(username, email, password1)

    # add instance to database
    db.session.add(user)
    # commit to databse
    db.session.commit()

    msg = Message(
        f"Welcome to Shoha's Bike Shop!",
        body= 'Thank you for joining our mailing list. We sell only the biest bikes. Stay tuned for more deals and fire cops.',
        recipients=[email]
    )

    mail.send(msg)

    return {
        'status': 'ok',
        'message': f"Successfully created an account for {username}.",
        'user': user.to_dict()
    }



@auth.route('/api/login', methods=["POST"])
def apiLogMeIn():
    data = request.json
    
        
    username = data['username']
    password = data['password']

    # check if user exists
    user = User.query.filter_by(username=username).first()

    if user:
        if check_password_hash(user.password, password):
            return {
                'status': 'ok',
                'message': f"Welcome back, {username}",
                'user': user.to_dict()
            }
        else:
            return {
                'status': 'not ok',
                'message': "Invalid password."
            }
    else:
        return {
            'status': "not ok",
            'message': "A user with that username does not exist."
        }

