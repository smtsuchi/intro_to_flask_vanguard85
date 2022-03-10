from flask import Blueprint, render_template, redirect, request, url_for
# import forms and models
from .forms import UserCreationForm
from app.models import User


auth = Blueprint('auth', __name__, template_folder='auth_templates')

from app.models import db

@auth.route('/login')
def logMeIn():
    return render_template('login.html')

@auth.route('/signup', methods=["GET", "POST"])
def signMeUp():
    form = UserCreationForm()
    if request.method == "POST":
        if form.validate():
            username = form.username.data
            email = form.email.data
            password = form.password.data

            # create an instance of our user
            user = User(username, email, password)

            # add instance to database
            db.session.add(user)
            # commit to databse
            db.session.commit()
            return redirect(url_for('auth.logMeIn'))
        else:
            print('did not validate')

    return render_template('signup.html', form=form)