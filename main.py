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


@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(username=email).first()
        if user and user.password == password:
            session['email'] = email
            flash("Logged in")
            return redirect('/new-post')
        elif user and user.password != password:
            flash('Password incorrect', 'error')
            return redirect('/login')
        elif not user:
            flash('User does not exist', 'error')
            return redirect('/login')

    return render_template('login.html')


@app.route('/signup', methods=['POST', 'GET'])
def signup():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        verify = request.form['verify']

        if (not email) or (email.strip() == ""):
            flash("Please enter a username.")
            return redirect("/signup")

        if (not password) or (password.strip() == ""):
            flash("Please enter a password.")
            return render_template('signup.html', email=email)

        if len(password) < 3 or len(password) > 20:
            flash("Passwords should be between 3 and 20 characters.")
            return render_template('signup.html', email=email)

        if (not verify) or (verify.strip() == ""):
            flash("Please re-enter your password.")
            return render_template('signup.html', email=email)

        if verify != password:
            flash("Please re-enter your password.")
            return render_template('signup.html', email=email)
        
        if (email) and (email.strip() != ""):
            if "@" not in email or "." not in email:
                flash("Please enter a valid email address.")
                return render_template('signup.html', email=email)
        
            if len(email) < 3 or len(email) > 20:
                flash("Emails should be between 3 and 20 characters.")
                return render_template('signup.html', email=email)

        existing_user = User.query.filter_by(username=email).first()
        if not existing_user:
            new_user = User(email, password)
            db.session.add(new_user)
            db.session.commit()
            session['email'] = email
            return redirect('/new-post')
        else:
            flash("Duplicate User")
            return redirect("/signup")

    return render_template('signup.html')

@app.route('/logout')
def logout():
    del session['email']
    return redirect('/login')

@app.route('/blog', methods=['POST', 'GET'])
def blog():

    blog_posts = Blog_Post.query.filter_by(user=session['email']).all()
    entry_id = request.args.get('id')
    if entry_id:
        blog_entry = Blog_Post.query.filter_by(id=entry_id).first()
        return render_template('blog-entry.html', title="Build a Blog!", blog_entry=blog_entry)
    return render_template('blog.html', title="Build a Blog!", blog_posts=blog_posts)


@app.route('/new-post', methods=['POST', 'GET'])
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