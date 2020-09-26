from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField
from wtforms.validators import DataRequired

class TopicForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    submit = SubmitField('Post')

class MessageForm(FlaskForm):
    content = TextAreaField('Content', validators=[DataRequired()])
    submit = SubmitField('Post')

class ThoughtForm(FlaskForm):
    content = TextAreaField('Content', validators=[DataRequired()])
    submit = SubmitField('Post')

class SearchForm(FlaskForm):
    search = StringField('')
    submit = SubmitField('Search')