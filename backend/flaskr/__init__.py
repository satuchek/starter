import os
from flask import Flask, request, abort, jsonify
from flask_cors import CORS
import json

from sqlalchemy.sql.expression import null

from models import db_drop_and_create_all, setup_db, Actor, Movie, CastList, db
from .auth.auth import AuthError, requires_auth

def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  setup_db(app)
  #app.config.from_object('config')
  CORS(app)


  @app.route('/actors')
  def get_all_actors():
    selection = Actor.query.all()
    actors = [actor.short() for actor in selection]
    return jsonify({
      'success': True,
      'actors': actors
    })

  @app.route('/actors', methods=['POST'])
  @requires_auth('post:actors')
  def create_actor(payload):
    request_data = request.get_json()
    if request_data is None:
      abort(400)
    try:
      new_name = request_data.get('name')
      new_age = request_data.get('age')
      new_image_link = request_data.get('image_link')
      new_imdb_link = request_data.get('imdb_link')
      new_gender = request_data.get('gender')
      new_seeking_roles = request_data.get('seeking_roles')
      new_seeking_description = request_data.get('seeking_description')
      actor = Actor(name=new_name, age=new_age, image_link=new_image_link, imdb_link=new_imdb_link, gender=new_gender, seeking_roles=new_seeking_roles, seeking_description=new_seeking_description)
      actor.insert()
      return jsonify({'success': True, 'id': actor.id})
    except:
      abort(422)

  @app.route('/actors/<int:actor_id>', methods=['PATCH'])
  @requires_auth('patch:actors')
  def update_actor(payload, actor_id):
    request_data = request.get_json()
    actor = Actor.query.filter(Actor.id == actor_id).one_or_none()
    if actor is None:
        abort(404)
    try:
      if 'name' in request_data:
        new_name = request_data.get('name')
        actor.name = new_name
      if 'age' in request_data:
        new_age = request_data.get('age')
        actor.age = new_age
      if 'image_link' in request_data:
        new_image_link = request_data.get('image_link')
        actor.image_link = new_image_link
      if 'imdb_link' in request_data:
        new_imdb_link = request_data.get('imdb_link')
        actor.imdb_link = new_imdb_link
      if 'gender' in request_data:
        new_gender = request_data.get('gender')
        actor.gender = new_gender
      if 'seeking_roles' in request_data:
        new_seeking_roles = request_data.get('seeking_roles')
        actor.seeking_roles = new_seeking_roles
      if 'seeking_description' in request_data:
        new_seeking_description = request_data.get('seeking_description')
        actor.seeking_description = new_seeking_description
      actor.update()
      return jsonify({'success': True, 'actor': actor.short()})
    except:
      abort(422)

  @app.route('/actors/<int:actor_id>')
  def get_actor_details(actor_id):
    selection = Actor.query.filter(Actor.id == actor_id).one_or_none()
    if selection is None:
      abort(404)
    actor = selection.format()

    return jsonify({'success': True, 'actor': actor})

  @app.route('/actors/<int:actor_id>', methods=['DELETE'])
  @requires_auth('delete:actors')
  def delete_actor(payload, actor_id):
    actor = Actor.query.filter(Actor.id == actor_id).one_or_none()
    if actor is None:
      abort(404)
    deleted_id = actor.id
    actor.delete()
    return jsonify({'success': True, 'id': deleted_id})

  @app.route('/actors/search', methods=['POST'])
  def search_actors():
    request_data = request.get_json()
    try:
      data = []
      query_result = Actor.query.filter(Actor.name.ilike('%' + request_data.get('search_term') + '%')).all()
      for actor in query_result:
        data.append(actor.short())
      response = {
        "success": True,
        "count": len(data),
        "actors": data
      }
      return response;
    except:
      abort(422)


  @app.route('/movies')
  def get_all_movies():
    selection = Movie.query.all()
    movies = [movie.short() for movie in selection]
    return jsonify({
      'success': True,
      'movies': movies
    })

  @app.route('/movies/<int:movie_id>')
  def get_movie_details(movie_id):
    selection = Movie.query.filter(Movie.id == movie_id).one_or_none()
    if selection is None:
      abort(404)
    return jsonify({'success': True, 'movie': selection.format()})

  @app.route('/movies/<int:movie_id>', methods=['DELETE'])
  @requires_auth('delete:movies')
  def delete_movie(payload, movie_id):
    movie = Movie.query.filter(Movie.id == movie_id).one_or_none()
    if movie is None:
      abort(404)
    deleted_id = movie.id
    movie.delete()
    return jsonify({'success': True, 'id': deleted_id})

  @app.route('/movies', methods=['POST'])
  @requires_auth('post:movies')
  def create_movie(payload):
    request_data = request.get_json()
    if request_data is None:
      abort(400)
    try:
      new_title = request_data.get('title')
      if 'image_link' in request_data:
        new_image_link = request_data.get('image_link')
      else:
        new_image_link = None
      if 'imdb_link' in request_data:
        new_imdb_link = request_data.get('imdb_link')
      else:
        new_imdb_link = None
      if 'release_date' in request_data:
        new_release_date = request_data.get('release_date')
      else:
        new_release_date = None
      if 'seeking_description' in request_data:
        new_seeking_description = request_data.get('seeking_description')
      else:
        new_seeking_description = None
      new_seeking_talent = request_data.get('seeking_talent')
      movie = Movie(title=new_title, image_link=new_image_link, imdb_link=new_imdb_link, \
        release_date=new_release_date, seeking_talent=new_seeking_talent, seeking_description=new_seeking_description)
      movie.insert()
      return jsonify({'success': True, 'id': movie.id})
    except:
      abort(422)

  @app.route('/movies/<int:movie_id>', methods=['PATCH'])
  @requires_auth('patch:movies')
  def update_movie(payload, movie_id):
    request_data = request.get_json()
    movie = Movie.query.filter(Movie.id == movie_id).one_or_none()
    if movie is None:
      abort(404)
    try:
      if 'title' in request_data:
        new_title = request_data.get('title')
        movie.title = new_title
      if 'image_link' in request_data:
        new_image_link = request_data.get('image_link')
        movie.image_link = new_image_link
      if 'imdb_link' in request_data:
        new_imdb_link = request_data.get('imdb_link')
        movie.imdb_link = new_imdb_link
      if 'release_date' in request_data:
        new_release_date = request_data.get('release_date')
        movie.release_date = new_release_date
      if 'seeking_talent' in request_data:
        new_seeking_talent = request_data.get('seeking_talent')
        movie.seeking_talent = new_seeking_talent
      if 'seeking_description' in request_data:
        new_seeking_description = request_data.get('seeking_description')
        movie.seeking_description = new_seeking_description
      movie.update()
      return jsonify({'success': True, 'movie': movie.short()})
    except:
      abort(422)

  @app.route('/movies/search', methods=['POST'])
  def search_movies():
    request_data = request.get_json()
    try:
      data = []
      query_result = Movie.query.filter(Movie.title.ilike('%' + request_data.get('search_term') + '%')).all()
      for movie in query_result:
        data.append(movie.format())
      response = {
        "success": True,
        "count": len(query_result),
        "movies": data
      }
      return response
    except:
      abort(422)

  @app.route('/castlist/actors/<int:actor_id>')
  def get_movies_for_actor(actor_id):
    data = []
    query_result = db.session.query(CastList.id, CastList.actor_id, CastList.movie_id, Movie.title, Movie.image_link)\
      .join(Movie, CastList.movie_id == Movie.id)\
      .filter(CastList.actor_id == actor_id)\
      .all()
    for item in query_result:
      obj = {
        "title": item.title,
        "image_link": item.image_link,
        "id": item.movie_id
      }
      data.append(obj)
    return jsonify({
      'success': True,
      'count': len(data),
      'movies': data
    })

  @app.route('/castlist/movies/<int:movie_id>')
  def get_cast_for_movie(movie_id):
    data = []
    query_result = db.session.query(CastList.id, CastList.actor_id, CastList.movie_id, Actor.name, Actor.image_link)\
      .join(Actor, CastList.actor_id == Actor.id)\
      .filter(CastList.movie_id == movie_id)\
      .all()
    for item in query_result:
      print(item)
      obj = {
        "name": item.name,
        "image_link": item.image_link,
        "id": item.actor_id
      }
      data.append(obj)
    return jsonify({
      'success': True,
      'count': len(data),
      'actors': data
    })

  @app.route('/castlist', methods=['POST'])
  @requires_auth('post:castlists')
  def create_castlist(payload):
    request_data = request.get_json()
    if request_data is None:
      abort(400)
    try:
      new_actor_id = request_data.get('actor_id')
      new_movie_id = request_data.get('movie_id')
      # No duplicates
      castlist_query = CastList.query.filter(CastList.movie_id == new_movie_id, CastList.actor_id == new_actor_id).one_or_none()
      if castlist_query is not None:
        abort(422)
      castlist = CastList(actor_id=new_actor_id, movie_id=new_movie_id)
      castlist.insert()
      return jsonify({'success': True})
    except:
      abort(422)

  @app.route('/castlist', methods=['DELETE'])
  @requires_auth('delete:castlists')
  def delete_castlist(payload):
    request_data = request.get_json()
    try:
      new_actor_id = request_data.get('actor_id')
      new_movie_id = request_data.get('movie_id')
    except:
      abort(400)
    # No duplicates
    castlist = CastList.query.filter(CastList.movie_id == new_movie_id, CastList.actor_id == new_actor_id).one_or_none()
    if castlist is None:
      abort(404)
    try:
      deleted_id = castlist.id
      castlist.delete()
      return jsonify({'success': True, 'id': deleted_id})
    except:
      abort(422)



  """ Error Handlers """
  @app.errorhandler(404)
  def not_found(error):
    return jsonify({
      'success': False,
      'error': 404,
      'message': 'resource not found'
    }), 404
    
  @app.errorhandler(422)
  def unprocessable(error):
    return jsonify({
      'success': False,
      'error': 422,
      'message': 'unprocessable'
    }), 422

  @app.errorhandler(405)
  def method_not_allowed(error):
    return jsonify({
      'success': False,
      'error': 405,
      'message': 'method not allowed'
    }), 405

  @app.errorhandler(400)
  def bad_request(error):
    return jsonify({
      "success": False, 
      "error": 400,
      "message": "bad request"
      }), 400

  @app.errorhandler(500)
  def interal_server_error(error):
    return jsonify({
      "success": False, 
      "error": 500,
      "message": "internal server error"
      }), 500

  @app.errorhandler(AuthError)
  def auth_error(error):
    return jsonify({
      'success': False,
      'error': error.status_code,
      'message': error.error.get('description')
    }), error.status_code

  return app

  



