"""Server for movie ratings app."""

from flask import (Flask, render_template, request, flash, session,
                   redirect)
from model import connect_to_db, db
import crud
from jinja2 import StrictUndefined

app = Flask(__name__)
app.secret_key = "dev"
app.jinja_env.undefined = StrictUndefined

@app.route('/')
def show_homepage():
    """View homepage."""
    print("hi") 

    return render_template('homepage.html')


@app.route('/movies')
def show_all_movies():

    all_movies = crud.get_movies()

    return render_template('all_movies.html', all_movies = all_movies)


@app.route('/movies/<movie_id>')
def show_movie(movie_id):

    return render_template('movie_details.html', movie=crud.get_movie_by_id(movie_id))
    


if __name__ == "__main__":
    connect_to_db(app)
    app.run(host="0.0.0.0", debug=True)
