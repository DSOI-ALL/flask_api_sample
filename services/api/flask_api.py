#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Flask, jsonify, abort, request, url_for, g
from flask.ext.httpauth import HTTPBasicAuth
from models import movies, users, User

auth = HTTPBasicAuth()

app = Flask(__name__)


@app.route("/api/movies/", methods=['GET'])
@auth.login_required
def get_all_movies():
    """
    only called in response to a 'GET' request.

    return a list of all movie objects
    """
    limit = int(request.args.get('limit', 10))
    offset = int(request.args.get('offset', 0))
    end = limit + offset

    filter_query = request.args.get('filter', None)

    return_movies = []

    if filter_query:
        filter_query = filter_query.replace("+"," ")
        filters = filter_query.split(',')
        for filter_str in filters:
            [return_movies.append(movie) for movie in movies[offset:end] if filter_str in movie.values()]
            # Using list comprehesion to say:
            # for movie in movies[offset:end]:
            #   if filter_str in movie.values():
            #       return_movies.append(movie)

    else:
        return_movies = movies[offset:end]


    return jsonify({"movies": return_movies})

    # Uncomment to return a URI rather than strict ID for objects.
    # return jsonify({'movies': [convert_id_to_uri(movie) for movie in return_movies]})


@app.route('/api/movies/', methods=['POST'])
@auth.login_required
def create_movie_object():
    """
    only called in response to a 'POST' request.

    Creates and persists a new movie object

    return the saved movie object
    """

    # Check to see if the json is there, and if it has the required fields.
    if not request.json or not 'Title' in request.json or not 'Year' in request.json:
        abort(400, {'message': 'Required fields Title, Year not in request.'})
        # abort(400)

    # Generate a new object from the request to save to DB.
    movie = {
        'id': movies[-1]['id'] + 1,
        'Title': request.json['Title'],
        'Plot': request.json.get('Plot', u""),
        'Year': request.json['Year'],
        'Rated': request.json.get('Rated', u""),
        'Released': request.json.get('Released', u""),
        'Runtime': request.json.get('Runtime', u""),
        'Genre': request.json.get('Genre', u""),
        'Director': request.json.get('Director', u""),
        'Writer': request.json.get('Writer', u""),
        'Actors': request.json.get('Actors', u""),
        'Language': request.json.get('Language', u""),
        'Country': request.json.get('Country', u""),
        'Awards': request.json.get('Awards', u""),
        'Poster': request.json.get('Poster', u""),
        'Metascore': request.json.get('Metascore', u""),
        'imdbRating': request.json.get('imdbRating', u"")
    }

    # save the new object. If you using an ORM, would be something like
    # object.save()
    movies.append(movie)

    return jsonify({'movie': movie}), 201


@app.route('/api/movies/<int:movie_id>', methods=['GET'])
@auth.login_required
def get_movie_by_id(movie_id):
    """
    only called in response to a 'GET' request.

    return a movie object by id
    """
    movie = [movie for movie in movies if movie['id'] == movie_id]

    if len(movie) == 0:
        abort(404)

    return jsonify({'movie': movie[0]})
    # return jsonify({'movie': convert_id_to_uri(movie[0])})


@app.route('/api/movies/<int:movie_id>', methods=['PUT'])
@auth.login_required
def update_task(movie_id):

    # Get the object to update
    movie = [movie for movie in movies if movie['id'] == movie_id]

    # Validate the data
    # Does the object exits?
    if len(movie) == 0:
        abort(404)

    # Is there json in the request?
    if not request.json:
        abort(400, {'message': 'No json found in request'})

    # Are the values valid types?
    for key in movie[0]:
        if key in request.json and type(request.json[key]) is not type(movie[0][key]):
            message = "%s is %s. %s passed in from request" % (key, type(movie[0][key]), type(request.json[key]))
            abort(400, {'message': message})

    # This is a sample:
    # We could write a test case for each field individually.
    # if 'Title' in request.json and type(request.json['Title']) != unicode:
    #     abort(400, {'message': 'Title is not unicode'})

    # Once everything looks good, update the object.
    # Here we are saying use the value from the request if it exists,
    # otherwise, default to the value already stored.
    for key, value in movie[0].iteritems():
        if key is not 'id':
            print "%s > JSON: %s || Object: %s" % (key, request.json.get(key, "Not here"), str(value))
            movie[0][key] = request.json.get(key, value)

    return jsonify({'movie': movie[0]})


@app.route('/api/movies/<int:movie_id>', methods=['DELETE'])
@auth.login_required
def delete_task(movie_id):
    # Get the object to delete
    movie = [movie for movie in movies if movie['id'] == movie_id]

    # Does the object exits?
    if len(movie) == 0:
        abort(404)

    # Delete the object from the data store
    movies.remove(movie[0])

    # Return success!
    return jsonify({'result': True})


@app.route('/api/users/', methods=['GET'])
def get_users():

    # tmp_user = []

    # for user in users:
    #     tmp_user.append(user.get_json())

    return jsonify({"users":[user.get_json() for user in users]})


@app.route('/api/users/', methods=['POST'])
def create_user():
    """
    only called in response to a 'POST' request.

    Creates and persists a new user object

    return the saved user object
    """

    # Check to see if the json is there, and if it has the required fields.
    if not request.json or not 'user' in request.json or not 'password' in request.json:
        abort(400, {'message': 'Required fields "user", "password" not in request.'})

    user = User(request.json['user'], request.json['password'])

    # save the new object. If you using an ORM, would be something like
    # object.save()
    user.save()

    return jsonify({'user': user.get_json()}), 201


@auth.verify_password
def verify_password(username, password):
    user = [user for user in users if user.username == username]
    if len(user) == 0 or not user[0].verify_password(password):
        return False
    g.user = user[0]
    return True


#########################
# Custom Error Handling #
#########################

@app.errorhandler(400)
def custom400(error):
    response = jsonify({'message': error.description['message'],
                        'status_code': 400,
                        'status': 'Bad Request'})
    return response, 400


####################
# Helper Functions #
####################


def convert_id_to_uri(movie):
    tmp = {}
    for field in movie:
        if field == 'id':
            tmp['uri'] = url_for('get_movie_by_id',
                                 movie_id=movie['id'],
                                 _external=True)
        else:
            tmp[field] = movie[field]
    return tmp


if __name__ == "__main__":
    user = User("twaits", "Passphrase1")
    user.save()
    print user.__dict__
    app.run(debug=True)
