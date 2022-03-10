from flask import Blueprint, render_template

ig = Blueprint('ig', __name__, template_folder='ig_templates')


@ig.route('/posts')
def posts():
    return render_template('login.html')

@ig.route('/create-posts')
def createPost():
    return render_template('signup.html')