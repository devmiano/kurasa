from flask import render_template,redirect,url_for,flash,request
from flask_login import login_user,logout_user, login_required

from .. import db
from . import auth