###########################
# Things which need to be addressed:
#     The "thoughts" are being eaten; not yet populating where I thought they should
#     Search function is laughable; I wanted to try the macro feature for the first time,
#         but it clearly needs some work
#     Message update/delete routes are dead. Need to be implemented
#############################


from flask import *
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from forms import SearchForm, TopicForm, MessageForm, ThoughtForm


app = Flask(__name__)
app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)




class Post(db.Model):
    __tablename__ = 'post'
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    title = db.Column(db.String(50), nullable=False)
    posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    messages = db.relationship('Message', backref='title', lazy='dynamic')

    def get_messages(self):
        return Message.query.filter_by(post_id=Post.id).order_by(Message.posted.desc())



class Message(db.Model):
    __tablename__ = 'message'
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    content = db.Column(db.String, nullable=False)
    posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'))
    thoughts = db.relationship('Thought', backref='title', lazy='dynamic')

    def get_thoughts(self):
        return Thought.query.filter_by(message_id=Message.id).order_by(Thought.posted.desc())



class Thought(db.Model):
    __tablename__ = 'thoughts'
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    content = db.Column(db.String, nullable=False)
    posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    message_id = db.Column(db.Integer, db.ForeignKey('message.id'))




@app.route('/', methods=['GET', 'POST'])
def index():
    search = SearchForm(request.form)
    posts = Post.query.all()
    
    if request.method == 'POST':
        return search_results(search)

    return render_template('home.html', posts=posts, form=search)


@app.route('/results')
def search_results(search):
    results = []
    search_string = search.data['search']
    if search.data['search'] == '':
        qry = db.session.query(Post.title)
        results = qry.all()
    if not results:
        flash('No results found!')
        return redirect('/')
    else:
        # display results
        return render_template('results.html', results=results)



@app.route("/post/new", methods=['GET', 'POST'])
def new_post():
    form = TopicForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data)
        db.session.add(post)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('create_topic.html', form=form, legend='New Topic') 
    

@app.route("/post/<int:post_id>")
def post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('post.html', post=post)


@app.route("/post/<int:post_id>/edit", methods=['GET', 'POST'])
def update_post(post_id):
    post = Post.query.get_or_404(post_id)

    form = TopicForm()
    if form.validate_on_submit():
        post.title = form.title.data
        db.session.commit()
        return redirect(url_for('post', post_id=post.id))
    elif request.method == 'GET':
        form.title.data = post.title

    return render_template('create_post.html', form=form)


@app.route("/post/<int:post_id>/delete", methods=['GET', 'POST'])
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    db.session.delete(post)
    db.session.commit()
    
    return redirect(url_for('index'))


@app.route("/message/<int:message_id>")
def message(message_id):
    message = Message.query.get_or_404(message_id)
    return render_template('message.html', message=message)


@app.route("/post/<int:post_id>/message", methods=['GET', 'POST'])
def new_message(post_id):
    form = MessageForm()
    if form.validate_on_submit():
        post = Message(content=form.content.data, post_id=post_id)
        db.session.add(post)
        db.session.commit()

        return redirect(url_for('index'))

    return render_template('create_post.html', form=form, legend='New Message')



# @app.route("/message/<int:message_id>/edit", methods=['GET', 'POST'])
# def update_message(message_id):
#     post = Message.query.get_or_404(message_id)

#     form = MessageForm()
#     if form.validate_on_submit():
#         message.content = form.content.data
#         db.session.commit()
#         return redirect(url_for('message', message_id=message_id))
#     elif request.method == 'GET':
#         form.content.data = message.content

#     return render_template('create_post.html', form=form)


# @app.route("/message/<int:message_id>/delete", methods=['GET', 'POST'])
# def delete_message(message_id):
#     post = Message.query.get_or_404(message_id)
#     db.session.delete(post)
#     db.session.commit()
    
#     return redirect(url_for('index'))


@app.route("/post/<int:message_id>/message", methods=['GET', 'POST'])
def new_thought(message_id):
    form = ThoughtForm()
    if form.validate_on_submit():
        post = Thought(content=form.content.data, message_id=message_id)
        db.session.add(post)
        db.session.commit()

        return redirect(url_for('index'))

    return render_template('create_post.html', form=form, legend='New Thought')


if __name__ == '__main__':
    app.run(debug=True)