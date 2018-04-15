from flask import Flask, request, redirect, render_template, session, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI']  ='mysql+pymysql://build-a-blog:thisisthepassword@localhost:8889/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)
app.secret_key = 'y337kGcys&zP3B'


class Blog_Post(db.Model): 

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120))
    body = db.Column(db.String(8000))

    def __init__(self, name, body):
        self.name = name
        self.body = body
        



@app.route('/', methods=['POST', 'GET'])
def index():


    if request.method == 'POST':
        post_name = request.form['blog_post']
        post_body = request.form['blog_text']
        new_post = Blog_Post(post_name, post_body)
        db.session.add(new_post)
        db.session.commit()
        

    blog_posts = Blog_Post.query.all()
    return render_template('new-post.html', title="Build a Blog!", 
    blog_posts=blog_posts)




if __name__ == '__main__':
    app.run()