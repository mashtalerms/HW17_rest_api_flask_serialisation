from app import Movie, Director, Genre
from flask_sqlalchemy import SQLAlchemy
from flask import Flask

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///lesson17_project_source/test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config["JSON_AS_ASCII"] = False
app.config['RESTX_JSON'] = {'ensure_ascii': False, 'indent': 3}
db = SQLAlchemy(app)


def check_if_director_is_in_list(director_id):
    last_director = db.session.query(Director).order_by(Director.id.desc()).first()
    if int(director_id) > last_director.id:
        return False
    return True


def check_if_genre_is_in_list(genre_id):
    last_genre = db.session.query(Genre).order_by(Genre.id.desc()).first()
    if int(genre_id) > last_genre.id:
        return False
    return True


def get_films_with_director(director_id):
    director = db.session.query(Director).filter(Director.id == director_id).one()
    films_with_director = []
    movies = Movie.query.all()
    for movie in movies:
        if movie.director_id == director.id:
            films_with_director.append(movie)
    return films_with_director


def get_films_with_genre(genre_id):
    genre = db.session.query(Genre).filter(Genre.id == genre_id).one()
    films_with_genre = []
    movies = Movie.query.all()
    for movie in movies:
        if movie.genre_id == genre.id:
            films_with_genre.append(movie)
    return films_with_genre


def get_films_with_director_and_genre(director_id, genre_id):
    director = db.session.query(Director).filter(Director.id == director_id).one()
    genre = db.session.query(Genre).filter(Genre.id == genre_id).one()
    films_with_director_and_genre = []
    movies = Movie.query.all()
    for movie in movies:
        if movie.director_id == director.id and movie.genre_id == genre.id:
            films_with_director_and_genre.append(movie)
    return films_with_director_and_genre
