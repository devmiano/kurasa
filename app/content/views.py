from flask import render_template, request, redirect, url_for, abort
from flask_login import login_required, current_user
from datetime import datetime as dt

from app.content.forms import AddBlog, AddComment
from app.requests import get_quotes
from ..models import Blog, User, Comment
from .. import db, photos
from . import content


@content.route('/<blog_id>')
def index(blog_id):
  blog = Blog.query.filter_by(id=blog_id).first()
  quote = get_quotes()
  title = f'{blog.title}'
  return render_template('content/content.html', title=title, blog_id=blog.id, blog=blog, quote=quote)


@content.route('/<uname>/new',methods=['GET', 'POST'])
def create(uname):
  user = User.query.filter_by(username=uname).first()
  '''function that renders the homepage'''
  
  form = AddBlog()
  now = dt.now()
  
  if form.validate_on_submit():
    title = form.title.data
    caption = form.caption.data
    content = form.content.data
    posted = now.strftime("%a %d %b %Y %I:%M:%S")
    author_id = current_user._get_current_object().id
    
    blog = Blog(title=title, caption=caption, content=content, posted=posted, author_id=author_id)
    
    db.session.add(blog)
    db.session.commit()
    
    return redirect(url_for('main.index'))
 
  title = 'Create a new blog'
  return render_template('content/create.html', title=title, form=form, uname=user.username,)


