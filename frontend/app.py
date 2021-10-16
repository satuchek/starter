import json
import dateutil.parser
import babel
from flask import Flask, render_template, request, Response, flash, redirect, url_for, abort, jsonify
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
import logging
from logging import Formatter, FileHandler
from flask_wtf import Form
from forms import *
import requests
from config import REQUEST_ADDRESS



app = Flask(__name__)
moment = Moment(app)
app.config.from_object('config')
# init db

def format_datetime(value, format='medium'):
  date = dateutil.parser.parse(value)
  if format == 'full':
      format="EEEE MMMM, d, y 'at' h:mma"
  elif format == 'medium':
      format="EE MM, dd, y h:mma"
  return babel.dates.format_datetime(date, format, locale='en')

app.jinja_env.filters['datetime'] = format_datetime

@app.route('/')
def index():
  return render_template('pages/home.html')



@app.route('/actors')
def actors():
    r = requests.get(REQUEST_ADDRESS + "/actors")
    data = r.json()

    return render_template('pages/actors.html', actors=data['actors'])

@app.route('/actors/create', methods=['GET'])
def create_actor_form():
    form = ActorForm()
    return render_template('forms/new_actor.html', form=form)

@app.route('/actors/create', methods=['POST'])
def create_actor_form_submission():
    form = ActorForm(request.form)
    error = False
    try:
        actor_name = form.name.data
        actor_age = form.age.data
        actor_image_link = form.image_link.data
        actor_imdb_link = form.imdb_link.data
        actor_gender = form.gender.data
        actor_seeking_roles = form.seeking_roles.data
        actor_seeking_description = form.seeking_description.data
        actor = {
            "name": actor_name, "age": actor_age, "gender": actor_gender,
            "image_link": actor_image_link, "imdb_link": actor_imdb_link,
            "seeking_roles": actor_seeking_roles, "seeking_description": actor_seeking_description
        }
        r = requests.post(REQUEST_ADDRESS + "/actors", json=actor)
        data = r.json()
        if not data['success']:
            error = True
    except:
        error = True
        flash('An error occurred. Actor could not be listed.')
    if error:
        return render_template('forms/new_actor.html', form=form)
    else:
        flash('Actor was successfully listed!')
        return render_template('pages/home.html')

@app.route('/actors/<int:actor_id>')
def show_actor(actor_id):
    r = requests.get(REQUEST_ADDRESS + "/actors/" + str(actor_id))
    data = r.json()
    r2 = requests.get(REQUEST_ADDRESS + "/castlist/actors/" + str(actor_id))
    movie = r2.json()

    return render_template('pages/show_actor.html', actor=data['actor'], count=movie['count'], movies=movie['movies'])

@app.route('/actors/search', methods=['POST'])
def search_actors():
    search = {'search_term': request.form.get('search_term')}
    r = requests.post(REQUEST_ADDRESS + "/actors/search", json=search)
    data = r.json()

    return render_template('pages/search_actors.html', results=data, search_term=request.form.get('search_term', ''))

@app.route('/actors/<int:actor_id>/edit', methods=['GET'])
def edit_actor(actor_id):
    form = ActorForm()
    r = requests.get(REQUEST_ADDRESS + "/actors/" + str(actor_id))
    data = r.json()

    form.gender.default = data['actor']['gender']
    form.process()
    return render_template('forms/edit_actor.html', form=form, actor=data['actor'])

@app.route('/actors/<int:actor_id>/edit', methods=['POST'])
def edit_actor_submission(actor_id):
    error = False
    form = ActorForm(request.form)
    try:
        name = form.name.data
        age = form.age.data
        image_link = form.image_link.data
        imdb_link = form.imdb_link.data
        gender = form.gender.data
        seeking_roles = form.seeking_roles.data
        seeking_description = form.seeking_description.data
        actor = {
            "name": name, "age": age, "gender": gender,
            "image_link": image_link, "imdb_link": imdb_link,
            "seeking_roles": seeking_roles, "seeking_description": seeking_description
        }
        r = requests.patch(REQUEST_ADDRESS + "/actors/" + str(actor_id), json=actor)
        data = r.json()
        if not data['success']:
            error = True
    except:
        error = True
    if error:
        flash('An error occurred. Actor ' + form.name.data + ' could not be edited.')
    else:
        flash('Actor ' + form.name.data + ' was successfully edited!')
    return redirect(url_for('show_actor', actor_id=actor_id))

@app.route('/movies')
def movies():
    r = requests.get(REQUEST_ADDRESS + "/movies")
    data = r.json()

    return render_template('pages/movies.html', movies=data['movies'])

@app.route('/movies/create', methods=['GET'])
def create_movie_form():
    form = MovieForm()
    return render_template('forms/new_movie.html', form=form)

@app.route('/movies/create', methods=['POST'])
def create_movie_form_submission():
    form = MovieForm(request.form)
    error = False
    try:
        movie_title = form.title.data
        movie_image_link = form.image_link.data
        movie_imdb_link = form.imdb_link.data
        movie_release_date = form.release_date.data.strftime('%Y-%m-%d')
        movie_seeking_talent = form.seeking_talent.data
        movie_seeking_description = form.seeking_description.data
        movie = {
            "title": movie_title, "image_link": movie_image_link, 
            "imdb_link": movie_imdb_link, "release_date": movie_release_date,
            "seeking_roles": movie_seeking_talent, "seeking_description": movie_seeking_description
        }
        r = requests.post(REQUEST_ADDRESS + "/movies", json=movie)
        data = r.json()
        if not data['success']:
            error = True
    except:
        error = True
        flash('An error occurred. Movie could not be listed.')
    if error:
        return render_template('forms/new_movie.html', form=form)
    else:
        flash('Movie was successfully listed!')
        return render_template('pages/home.html')

@app.route('/movies/<int:movie_id>')
def show_movie(movie_id):
    r = requests.get(REQUEST_ADDRESS + "/movies/" + str(movie_id))
    data = r.json()
    r2 = requests.get(REQUEST_ADDRESS + "/castlist/movies/" + str(movie_id))
    actor = r2.json()

    return render_template('pages/show_movie.html', movie=data['movie'], count=actor['count'], actors=actor['actors'])


@app.route('/movies/search', methods=['POST'])
def search_movies():
    search = {'search_term': request.form.get('search_term')}
    r = requests.post(REQUEST_ADDRESS + "/movies/search", json=search)
    data = r.json()
    print(data)

    return render_template('pages/search_movies.html', results=data, search_term=request.form.get('search_term', ''))

@app.route('/movies/<int:movie_id>/edit', methods=['GET'])
def edit_movie(movie_id):
    form = MovieForm()
    r = requests.get(REQUEST_ADDRESS + "/movies/" + str(movie_id))
    data = r.json()
    
    return render_template('forms/edit_movie.html', form=form, movie=data['movie'])

@app.route('/movies/<int:movie_id>/edit', methods=['POST'])
def edit_movie_submission(movie_id):
    error = False
    form = MovieForm(request.form)
    try:
        release_date = form.release_date.data.strftime('%Y-%m-%d')
        title = form.title.data
        image_link = form.image_link.data
        imdb_link = form.imdb_link.data
        seeking_talent = form.seeking_talent.data
        seeking_description = form.seeking_description.data
        movie = {
            "title": title, "release_date": release_date,
            "image_link": image_link, "imdb_link": imdb_link,
            "seeking_talent": seeking_talent, "seeking_description": seeking_description
        }
        r = requests.patch(REQUEST_ADDRESS + "/movies/" + str(movie_id), json=movie)
        data = r.json()
        if not data['success']:
            error = True
    except:
        error = True
    if error:
        flash('An error occurred. Movie ' + form.title.data + ' could not be edited.')
    else:
        flash('Movie ' + form.title.data + ' was successfully edited!')
    return redirect(url_for('show_movie', movie_id=movie_id))

@app.route('/castlist/update')
def create_castlist():
  # renders form. do not touch.
  form = CastlistForm()
  return render_template('forms/update_castlist.html', form=form)


@app.route('/castlist/update', methods=['POST'])
def create_castlist_submission():
  # called to create new shows in the db, upon submitting new show listing form
  # DONE: insert form data as a new Show record in the db, instead
  form = CastlistForm(request.form)
  error = False
  try:
    actor_id = form.actor_id.data
    movie_id = form.movie_id.data
    castlist = {
            "actor_id": actor_id, "movie_id": movie_id
    }
    r = requests.post(REQUEST_ADDRESS + "/castlist", json=castlist)
    data = r.json()
    if not data['success']:
        error = True
  except:
    error = True
  if error:
    flash('An error occurred. Actor could not be cast.')
    return render_template('forms/update_castlist.html', form=form)
  else:
    # on successful db insert, flash success
    flash('Actor was successfully cast!')
    return render_template('pages/home.html')

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080)
