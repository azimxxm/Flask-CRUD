from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Artice(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    intro = db.Column(db.String(300), nullable=False)
    text = db.Column(db.Text(5000), nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Article %r>' % self.id


@app.route('/')
@app.route('/home')
async def index():
    return render_template("index.html")


@app.route('/about')
async def about():
    return render_template("about.html")


@app.route('/posts')
async def posts():
    artile = Artice.query.order_by(Artice.date.desc()).all()
    return render_template("posts.html", artile=artile)


@app.route('/posts/<int:id>')
async def posts_detail(id):
    artiles = Artice.query.get(id)
    return render_template("posts_detail.html", artiles=artiles)


@app.route('/posts/<int:id>/delete')
async def posts_delete(id):
    artiles = Artice.query.get_or_404(id)
    try:
        db.session.delete(artiles)
        db.session.commit()
        return redirect('/posts')

    except:
        return "message: error"


@app.route('/posts/<int:id>/update', methods=['POST', 'GET'])
async def posts_update(id):
    artiles = Artice.query.get(id)
    if request.method == "POST":
        artiles.title = request.form['title']
        artiles.intro = request.form['intro']
        artiles.text = request.form['text']

        try:
            db.session.commit()
            return redirect('/posts')
        except:
            return "message: error"
    else:
        return render_template("post_update.html", artiles=artiles)


@app.route('/create-article', methods=['POST', 'GET'])
async def create_article():
    if request.method == "POST":
        title = request.form['title']
        intro = request.form['intro']
        text = request.form['text']

        article = Artice(title=title, intro=intro, text=text)
        try:
            db.session.add(article)
            db.session.commit()
            return redirect('/posts')
        except:
            return "message: error"
    else:
        return render_template("create-article.html")


# @app.route('/user/<string:name>/<int:id>')
# async def user(name, id):
#     return f"User page: {name} - {str(id)}"

if __name__ == "__main__":
    app.run(debug=True, host="localhost", port=8000)
