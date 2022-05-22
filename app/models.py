from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import UserMixin, current_user
from datetime import datetime
from . import db
from . import login_manager

@login_manager.user_loader
def load_user(user_id):
  return User.query.get(int(user_id))

class User(UserMixin, db.Model):
  __tablename__ = 'users'
  
  id = db.Column(db.Integer, primary_key=True)
  first_name = db.Column(db.String(255))
  last_name = db.Column(db.String(255))
  username = db.Column(db.String(255), unique=True, index=True)
  email = db.Column(db.String(255), unique=True, index=True)
  bio = db.Column(db.String(255))
  role = db.Column(db.String(255))
  profile_pic_path = db.Column(db.String(255))
  password_hash = db.Column(db.String(255))
  blogs = db.relationship('Blog', backref='user', lazy='dynamic')
  comments = db.relationship('Comment', backref='user', lazy='dynamic')
  created = db.Column(db.DateTime,default=datetime.utcnow)
  
  @property
  def password(self):
    raise AttributeError('you cannot read the password')
  
  @password.setter
  def password(self, password):
    self.password_hash = generate_password_hash(password)
    
  def verify_password(self, password):
    return check_password_hash(self.password_hash, password)
  
  def __repr__(self):
      return f'User {self.username}'
    
  
class Role(db.Model):
  __tablename__ = 'roles'
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(255), unique=True, index=True)
  title = db.Column(db.String(255))
  
  def __repr__(self):
    return f'{self.name}'
  
class Blog(db.Model):
  __tablename__ = 'blogs'
  id = db.Column(db.Integer, primary_key=True)
  title = db.Column(db.String(48), index = True)
  caption = db.Column(db.String(100))
  content = db.Column(db.String(255))
  blog_pic_path = db.Column(db.String(255))
  author_id = db.Column(db.Integer,db.ForeignKey("users.id"), nullable = False)
  comments = db.relationship('Comment', backref='blog', lazy='dynamic')
  posted = db.Column(db.DateTime,default=datetime.utcnow)
  
  def save_blog(self):
    db.session.add(self)
    db.session.commit()
  
  @classmethod
  def get_blogs(cls, id):
    blogs = Blog.query.order_by(blog_id=id).desc().all()
    return blogs
    
  
  def __repr__(self):
    return f'Pitch {self.caption}'
  
class Comment(db.Model):
  __tablename__ = 'comments'
  id = db.Column(db.Integer, primary_key=True)
  caption = db.Column(db.String(255))
  blog_id = db.Column(db.Integer, db.ForeignKey("blogs.id"), nullable= False)
  author_id = db.Column(db.Integer ,db.ForeignKey("users.id"), nullable=False)
  posted = db.Column(db.DateTime,default=datetime.utcnow)
  
  def save_comment(self):
    db.session.add(self)
    db.session.commit()
  
  def __repr__(self):
    return f'{self.caption}'