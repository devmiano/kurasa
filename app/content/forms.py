from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField,TextAreaField
from wtforms.validators import InputRequired,Length
  
class AddBlog(FlaskForm):
  title = StringField('Blog title', validators=[InputRequired(), Length(min=4, max=100)])
  caption = StringField('Short description', validators=[InputRequired(), Length(min=4, max=1000)])
  content = TextAreaField('Content', validators=[InputRequired(), Length(min=4, max=1000)])
  submit = SubmitField('Submit')
  
class AddComment(FlaskForm):
  caption = TextAreaField('Add your  comment')
  submit = SubmitField('Submit')