from flask import Flask, request, redirect, render_template
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:build-a-blog@localhost:8889/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)


# Create Blog class for database persistence
class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    body = db.Column(db.Text)
    pub_date = db.Column(db.DateTime, nullable=False,
        default=datetime.utcnow)

    def __init__(self, title, body, pub_date):
        self.title = title
        self.body = body
        self.pub_date = pub_date


@app.route("/blog")
def index():

    posts_list = Blog.query.get(all)

    return render_template('blog.html', posts=posts_list)

@app.route('/newpost', methods=['POST', 'GET'])
def create_post():

    # Create empty strings for error messages
    title_error = ""
    body_error = ""

    # Assign variables to arguments from newpost form
    post_title = request.form['blog_title']
    post_body =  request.form['blog_body']
    post_date = request.form['blog_date']
    new_post =  Blog(post_title, post_body, post_date)


if __name__ == "__main__":
    app.run()