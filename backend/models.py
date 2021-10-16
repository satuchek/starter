import os
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, String, Integer, Boolean, ForeignKey, Date
from config import DB_PATH
import json




db = SQLAlchemy()

def setup_db(app, database_path=DB_PATH):
  app.config["SQLALCHEMY_DATABASE_URI"] = database_path
  app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
  db.app = app
  db.init_app(app)
  db.create_all()

def db_drop_and_create_all():
    db.drop_all()
    db.create_all()
    # demo data for tests
    actor = Actor(name="Tom Hanks", age=45, image_link="", imdb_link="", gender="Male", seeking_roles=False, seeking_description="")
    actor.insert()

class Actor(db.Model):
    __tablename__ = 'actors'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    age = Column(Integer)
    image_link = Column(String(500))
    imdb_link = Column(String(500))
    seeking_roles = Column(Boolean, nullable=False, default=False)
    gender = Column(String, nullable=False)
    seeking_description = Column(db.String(120))

    def __init__(self, name, age, image_link, imdb_link, seeking_roles, gender, seeking_description):
      self.name = name
      self.age = age
      self.image_link = image_link
      self.imdb_link = imdb_link
      self.seeking_roles = seeking_roles
      self.seeking_description = seeking_description
      self.gender = gender
    
    def insert(self):
      db.session.add(self)
      db.session.commit()
    
    def update(self):
      db.session.commit()

    def delete(self):
      db.session.delete(self)
      db.session.commit()

    def short(self):
      return {
        'id': self.id,
        'name': self.name
    }

    def format(self):
      return{
        'id': self.id,
        'name': self.name,
        'age': self.age,
        'image_link': self.image_link,
        'seeking_roles': self.seeking_roles,
        'imdb_link': self.imdb_link,
        'seeking_description': self.seeking_description,
        'gender': self.gender
      }

    def __repr__(self):
      return f'<Actor ID: {self.id}, name: {self.name}, age: {self.age}, image_link: {self.image_link}, imdb_link: {self.imdb_link}, seeking_roles: {self.seeking_roles}, seeking_description: {self.seeking_description}, gender: {self.gender}>'

class Movie(db.Model):
    __tablename__ = 'movies'
    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    image_link = Column(String(500))
    imdb_link = Column(String(500))
    release_date = Column(Date)
    seeking_talent = Column(Boolean, nullable=False, default=False)
    seeking_description = Column(String(120))

    def __init__(self, title, image_link, imdb_link, seeking_talent, release_date, seeking_description):
      self.title = title     
      self.image_link = image_link
      self.imdb_link = imdb_link
      self.seeking_talent = seeking_talent
      self.seeking_description = seeking_description
      self.release_date = release_date
    
    def insert(self):
      db.session.add(self)
      db.session.commit()
    
    def update(self):
      db.session.commit()

    def delete(self):
      db.session.delete(self)
      db.session.commit()

    def short(self):
      return {
        'id': self.id,
        'title': self.title
    }

    def format(self):
      release_date = self.release_date if self.release_date is None else self.release_date.strftime('%Y-%m-%d')
      return {
        'id': self.id,
        'title': self.title,
        'image_link': self.image_link,
        'imdb_link': self.imdb_link,
        'release_date': release_date,
        'seeking_talent': self.seeking_talent,
        'seeking_description': self.seeking_description
    }

    def __repr__(self):
      return f'<Movie ID: {self.id}, title: {self.title}, image_link: {self.image_link}, release_date: {self.release_date}>'

class CastList(db.Model):
  __tablename__ = 'castlists'
  id = Column(Integer, primary_key=True)
  actor_id = Column(Integer, ForeignKey('actors.id', ondelete="CASCADE"), nullable=False)
  movie_id = Column(Integer, ForeignKey('movies.id', ondelete="CASCADE"), nullable=False)

  def __init__(self, actor_id, movie_id):
      self.actor_id = actor_id  
      self.movie_id = movie_id

  def insert(self):
    db.session.add(self)
    db.session.commit()
  
  def update(self):
    db.session.commit()

  def delete(self):
    db.session.delete(self)
    db.session.commit()



