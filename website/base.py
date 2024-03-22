from flask import Blueprint, render_template, request, flash, redirect, url_for, g, abort
from flask_login import login_required, current_user
from .models import Post
from . import db

base_bp = Blueprint("base", __name__)

@base_bp.route("/")
@login_required
def home():
    posts = Post.query.all()  # fetch all posts from the database
    return render_template('_base.html', posts=posts)

@base_bp.route('/create', methods=('GET', 'POST'))
@login_required
def create():
    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        error = None

        if not title:
            error = 'Title is required.'

        if error is not None:
            flash(error)
        else:
            new_post = Post(title=title, body=body, author_id=current_user.id)
            db.session.add(new_post)
            db.session.commit()
            flash('Your post was successfully created')
            return redirect(url_for('_base.home'))

    return render_template('create.html')

def get_post(id, check_author=True):
    post = Post.query.get(id)

    if post is None:
        abort(404, f"Post id {id} doesn't exist.")

    if check_author and post.author_id != current_user.id:
        abort(403)

    return post



base_bp.route('/update/<int:post_id>', methods=('GET', 'POST'))
@login_required
def update(post_id):
    post = Post.query.get(post_id)

    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        error = None

        if not title:
            error = 'Title is required.'

        if error is not None:
            flash(error)
        else:
            post.title = title
            post.body = body
            db.session.commit()
            flash('Your post was successfully updated')
            return redirect(url_for('_base.home'))

    return render_template('update.html', post=post)

@base_bp.route('/<int:id>/delete', methods=('POST',))
@login_required
def delete(id):
    post = get_post(id)
    if post is not None:
        db.session.delete(post)
        db.session.commit()
    return redirect(url_for('_base.home'))