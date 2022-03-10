from flask import Blueprint, redirect, render_template, request, url_for
from flask_login import current_user, login_required


ig = Blueprint('ig', __name__, template_folder='ig_templates')

from .forms import CreatePostForm
from app.models import db, Post


@ig.route('/posts')
def posts():
    posts = Post.query.all()[::-1]
    return render_template('posts.html', posts = posts)

@ig.route('/create-post', methods=["GET", "POST"])
@login_required
def createPost():
    form = CreatePostForm()
    if request.method == "POST":
        if form.validate():
            title = form.title.data
            img_url = form.img_url.data
            caption = form.caption.data

            post = Post(title, img_url, caption, current_user.id)

            db.session.add(post)
            db.session.commit()   

            return redirect(url_for('home'))         

    return render_template('createpost.html', form = form)