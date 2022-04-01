from flask import Blueprint, redirect, render_template, request, url_for
from flask_login import current_user, login_required


ig = Blueprint('ig', __name__, template_folder='ig_templates')

from .forms import CreatePostForm, UpdatePostForm
from app.models import db, Post, User


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

@ig.route('/posts/<int:post_id>')
def individualPost(post_id):
    post = Post.query.filter_by(id=post_id).first()
    if post is None:
        return redirect(url_for('ig.posts'))
    return render_template('individual_post.html', post = post)

@ig.route('/posts/update/<int:post_id>', methods=["GET","POST"])
@login_required
def updatePost(post_id):
    post = Post.query.filter_by(id=post_id).first()
    if post is None:
        return redirect(url_for('ig.posts'))
    if post.user_id != current_user.id:
        return redirect(url_for('ig.posts'))
    form = UpdatePostForm()
    if request.method == "POST":
        if form.validate():
            title = form.title.data
            img_url = form.img_url.data
            caption = form.caption.data

            # update the original post
            post.title = title
            post.image = img_url
            post.caption = caption

            db.session.commit()   

            return redirect(url_for('home'))         
    return render_template('updatepost.html', form=form, post = post)


@ig.route('/posts/delete/<int:post_id>', methods=["POST"])
@login_required
def deletePost(post_id):
    post = Post.query.filter_by(id=post_id).first()
    if post is None:
        return redirect(url_for('ig.posts'))
    if post.user_id != current_user.id:
        return redirect(url_for('ig.posts'))

    db.session.delete(post)
    db.session.commit()
               
    return redirect(url_for('ig.posts'))


# 
# 
#   API STARTS HERE
# 
#

@ig.route('/api/posts')
def apiPosts():
    posts = Post.query.all()[::-1]
    return {
        'status': 'ok',
        'total_results': len(posts),
        'posts': [p.to_dict() for p in posts]
        }

@ig.route('/api/posts/<int:post_id>')
def apiSinglePost(post_id):
    post = Post.query.filter_by(id=post_id).first()
    if post is None:
        return {
            'status': 'not ok',
            'total_results': 0,
        }
    return {
        'status': 'ok',
        'total_results': 1,
        'post': post.to_dict()
        }


@ig.route('/api/create-post', methods=["POST"])
# @login_required
def apiCreatePost():
    data = request.json

    title = data['title']
    img_url = data['img_url']
    caption = data['caption']
    token = data['token']

    user = User.query.filter_by(apitoken=token).first()

    if user is None:
        return {
            'status': 'not ok',
            'message': 'Invalid token.'
        }

    post = Post(title, img_url, caption, user.id)

    db.session.add(post)
    db.session.commit()   

    return {
        'status': 'ok',
        'message': 'Successfully create a new post.',
        'post': post.to_dict()
    }
