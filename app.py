# app.py

from flask import Flask, request, jsonify
from flask_restx import Api, Resource
from flask_sqlalchemy import SQLAlchemy
from marshmallow import Schema, fields
import utils


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///lesson17_project_source/test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config["JSON_AS_ASCII"] = False
app.config['RESTX_JSON'] = {'ensure_ascii': False, 'indent': 3}
db = SQLAlchemy(app)

api = Api(app)
movie_ns = api.namespace('movies')
director_ns = api.namespace('directors')
genre_ns = api.namespace('genres')


class Movie(db.Model):
    __tablename__ = 'movie'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))
    description = db.Column(db.String(255))
    trailer = db.Column(db.String(255))
    year = db.Column(db.Integer)
    rating = db.Column(db.Float)
    genre_id = db.Column(db.Integer, db.ForeignKey("genre.id"))
    genre = db.relationship("Genre")
    director_id = db.Column(db.Integer, db.ForeignKey("director.id"))
    director = db.relationship("Director")


class Director(db.Model):
    __tablename__ = 'director'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))


class Genre(db.Model):
    __tablename__ = 'genre'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))


class MovieSchema(Schema):
    id = fields.Int()
    title = fields.Str()
    description = fields.Str()
    trailer = fields.Str()
    year = fields.Int()
    rating = fields.Float()
    genre_id = fields.Int()
    director_id = fields.Int()


class DirectorSchema(Schema):
    id = fields.Int()
    name = fields.Str()


class GenreSchema(Schema):
    id = fields.Int()
    name = fields.Str()


movie_schema = MovieSchema()
movies_schema = MovieSchema(many=True)

director_schema = DirectorSchema()
genre_schema = GenreSchema()


@movie_ns.route('/')
class MovieView(Resource):
    def get(self):
        director_id = request.args.get("director_id")
        genre_id = request.args.get("genre_id")
        if not director_id and not genre_id:
            movies = Movie.query.all()
            return movies_schema.dump(movies), 200
        elif director_id and not genre_id:
            if not utils.check_if_director_is_in_list(director_id):
                return 'No such Director', 404
            else:
                return movies_schema.dump(utils.get_films_with_director(director_id)), 200
        elif genre_id and not director_id:
            if not utils.check_if_genre_is_in_list(genre_id):
                return 'No such Genre', 404
            else:
                return movies_schema.dump(utils.get_films_with_genre(genre_id)), 200
        elif director_id and genre_id:
            return movies_schema.dump(utils.get_films_with_director_and_genre(director_id, genre_id)), 200


@movie_ns.route('/<int:mid>')
class MovieView(Resource):
    def get(self, mid):
        movie = Movie.query.get(mid)
        return movie_schema.dump(movie), 200


@director_ns.route('/')
class DirectorView(Resource):
    def post(self):
        req_json = request.json
        director = Director(**req_json)
        with db.session.begin():
            db.session.add(director)
            db.session.commit()
        return director_schema.dump(director), 200


@director_ns.route('/<int:did>')
class DirectorView(Resource):
    def put(self, did):
        req_json = request.json
        director = Director.query.filter(Director.id == did).one()
        if not director:
            return "Not found 404", 404
        director.name = req_json.get('name')
        db.session.add(director)
        db.session.commit()
        return director_schema.dump(director), 200

    def delete(self, did):
        director = Director.query.get(did)
        if not director:
            return "Not found 404", 404
        db.session.delete(director)
        db.session.commit()
        return 'Director deleted!'


@genre_ns.route('/')
class GenreView(Resource):
    def post(self):
        req_json = request.json
        genre = Genre(**req_json)
        with db.session.begin():
            db.session.add(genre)
            db.session.commit()
        return genre_schema.dump(genre), 200


@genre_ns.route('/<int:gid>')
class DirectorView(Resource):
    def put(self, gid):
        req_json = request.json
        genre = Genre.query.filter(Genre.id == gid).one()
        if not genre:
            return "Not found 404", 404
        genre.name = req_json.get('name')
        db.session.add(genre)
        db.session.commit()
        return director_schema.dump(genre), 200

    def delete(self, gid):
        genre = Genre.query.get(gid)
        if not genre:
            return "Not found 404", 404
        db.session.delete(genre)
        db.session.commit()
        return 'Genre deleted!'


if __name__ == '__main__':
    app.run()
