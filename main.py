from flask import Flask, request, redirect, render_template, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["DEBUG"] = True
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://build-a-blog:build-a-blog@localhost:8889/build-a-blog"
app.config["SQLALCHEMY_ECHO"] = True
app.secret_key = "z!97tvMYD_E92zNVBGUq-_UzfGHQVk"
db = SQLAlchemy(app)


# Create Blog class for database persistence
class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    body = db.Column(db.Text)

    def __init__(self, title, body):
        self.title = title
        self.body = body


@app.route("/blog")
def index():
    post_id = request.args.get('id')

    if post_id:
        single_post = Blog.query.get(post_id)
        return render_template('single_post.html', single_post=single_post)
    else:
        all_posts = Blog.query.all()
        return render_template("blog.html", all_posts=all_posts)

@app.route("/newpost", methods=["POST", "GET"])
def add_post():

    if request.method == "POST":
        new_title = request.form["title"]
        new_body = request.form["body"]
        new_post = Blog(new_title, new_body)

        if len(new_title) != 0 and len(new_body) != 0:
            db.session.add(new_post)
            db.session.commit()

            post_link = f"/blog?id={new_post.id}"
            return redirect(post_link)

        else:
            flash("Posts require both a title and a body...try again!")
            return render_template("add_post.html", new_title=new_title, new_body=new_body, title="Add a Blog Entry")

    else:
        return render_template("add_post.html")
        

if __name__ == "__main__":
    app.run()