from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///filer.db'
db = SQLAlchemy(app)

# database being created here
class Movies(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False) # this means this field cannot be blank
    date_added = db.Column(db.DateTime, default=datetime.utcnow)
    def __repr__(self):
        return '<Movie %r>' % self.id

@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        movie_content = request.form['content']
        new_movie = Movies(name=movie_content)
        try:
            db.session.add(new_movie)
            db.session.commit() # this like the save() statement
            return redirect('/')
        except:
            return 'Problem adding that movie into the database'
    else:
        movies = Movies.query.order_by(Movies.date_added).all()
        return render_template('index.html',movies=movies)

@app.route('/delete/<int:id>')
def delete(id):
    deletingMovie = Movies.query.get_or_404(id)

    try:
        db.session.delete(deletingMovie)
        db.session.commit()
        return redirect('/')
    except:
        return 'That movie had a problem while deleting'

@app.route('/update/<int:id>', methods=['GET','POST'])
def update(id):
    updatingMovie = Movies.query.get_or_404(id)

    if request.method == 'POST':
        updatingMovie.name = request.form['content']
        try:
            db.session.commit()
            return redirect('/')
        except:
            return "That movie had an issue while updating"
    else:
        return render_template('update.html',movie=updatingMovie)


if __name__ == '__main__':
    app.run(debug=True)