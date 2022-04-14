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


@app.route('/users')
def show_all_users():

    all_users = crud.get_users()

    return render_template('all_users.html', all_users = all_users)

@app.route('/users', methods=['POST'])
def register_user():
    """Create a new user."""

    email = request.form.get('email')
    password = request.form.get('password')

    check = crud.get_user_by_email(email)
    if check == None:
        new_user = crud.create_user(email,password)
        db.session.add(new_user)
        db.session.commit()
    else:
        flash("Email already has an account. Try logging in instead.")

    return redirect('/')

@app.route('/login', methods=['POST'])
def login():
    '''sign into an account'''

    email = request.form.get('email')
    password = request.form.get('password')

    user = crud.get_user_by_email(email)

    if user == None:
        flash("Email doesn't exist. Try creating a login instead.")
    else:
        if user.password == password:
            session['user_id'] = user.user_id
            flash(f"You're logged in!, {session['user_id']}")
        else:
            flash("Wrong password")

    return redirect('/')


@app.route('/users/<user_id>')
def show_user(user_id):

    return render_template('user_details.html', user=crud.get_user_by_id(user_id))
    



if __name__ == "__main__":
    connect_to_db(app)
    app.run(host="0.0.0.0", debug=True)
