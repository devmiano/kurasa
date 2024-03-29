from flask import render_template,request,redirect,url_for,abort
from flask_login import login_required, current_user
from ..models import Blog, User, Comment
from app.main.forms import UpdateProfile
from datetime import datetime as dt

from .. import db,photos
from . import main

@main.route('/')
def index():
  '''function that renders the homepage'''
  title = 'Blog for Life'
  blog = Blog.query.order_by(Blog.posted.desc()).all()
 
  return render_template('index.html', title=title, blog=blog)


@main.route('/user/<uname>')
def profile(uname):
  
  user = User.query.filter_by(username=uname).first()
  author_id=current_user._get_current_object().id,
  
  if user is None:
    abort(404)
    
  title = f'{user.first_name} {user.last_name}'
    
  return render_template('profile/profile.html', user=user, title=title)


@main.route('/user/<uname>/update', methods=['GET', 'POST'])
@login_required
def update_profile(uname):
  user = User.query.filter_by(username=uname).first()
  
  if user is None:
    abort(404)
    
  update = UpdateProfile()
  
  if update.validate_on_submit():
    user.first_name = update.first_name.data
    user.last_name = update.last_name.data
    user.bio = update.bio.data
    
    
    db.session.add(user)
    db.session.commit()
    
    
    
    return redirect(url_for('.profile', uname=user.username))
  
  title = f'{user.first_name} {user.last_name} Update Profile'
    
  return render_template('profile/update.html', update=update, title=title)


@main.route('/user/<uname>/update/pic',methods= ['POST'])
@login_required
def update_pic(uname):
  user = User.query.filter_by(username=uname).first()
  if 'photo' in request.files:
    filename = photos.save(request.files['photo'])
    path = f'photos/{filename}'
    user.profile_pic_path = path
    db.session.commit()
    
    title = f'{user.first_name} {user.last_name} Update Pic'
    
  return redirect(url_for('main.profile', uname=uname))