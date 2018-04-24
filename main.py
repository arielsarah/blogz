from flask import Flask, request, redirect, render_template, session, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI']  ='mysql+pymysql://blogz:thisisthepassword@localhost:8889/blogz'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)
app.secret_key = 'y337kGcys&zP3B'


class Blog_Post(db.Model): 

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120))
    body = db.Column(db.String(8000))
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __init__(self, name, body, owner):
        self.name = name
        self.body = body
        self.owner = owner
        
class User(db.Model):

   id = db.Column(db.Integer, primary_key=True)
   username = db.Column(db.String(120))
   password = db.Column(db.String(120))
   blogs = db.relationship('Blog_Post', backref='owner')
   
   def __init__(self, username, password):
       self.username = username
       self.password = password


@app.route('/blog', methods=['POST', 'GET'])
def blog():

    blog_posts = Blog_Post.query.filter_by(user=session['email']).all()
    entry_id = request.args.get('id')
    if entry_id:
        blog_entry = Blog_Post.query.filter_by(id=entry_id).first()
        return render_template('blog-entry.html', title="Build a Blog!", blog_entry=blog_entry)
    return render_template('blog.html', title="Build a Blog!", blog_posts=blog_posts)


@app.route('/newpost', methods=['POST', 'GET'])
def newpost():
    if request.method == 'POST':
        post_name = request.form['blog_post']
        post_body = request.form['blog_text']
        post_owner = User.query.filter_by(email=session['user']).first()
        if post_name == "":
            flash("Please enter a Post Name")
            return render_template('new-post.html', title="Build a Blog!", blog_text=post_body)
        elif post_body == "":
            flash("Please enter a Blog Post")
            return render_template('new-post.html', title="Build a Blog!", blog_name=post_name)
        new_post = Blog_Post(post_name, post_body, post_owner)
        db.session.add(new_post)
        db.session.commit()
        return redirect('/blog?id='+ str(new_post.id))

    return render_template('new-post.html',title="Build a Blog!")

if __name__ == '__main__':
    app.run()