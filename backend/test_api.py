import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy
from config import TEST_DB_PATH

from flaskr import create_app
from models import setup_db, Actor, Movie, CastList, db_drop_and_create_all



class SpotlightTests(unittest.TestCase):
    """ This class represents the Spotlight API Tests """
    new_actor_id = -1
    new_movie_id = -1
    new_actor = {
        'name': 'Ryan Reynolds',
        'image_link': 'https://m.media-amazon.com/images/M/MV5BOTI3ODk1MTMyNV5BMl5BanBnXkFtZTcwNDEyNTE2Mg@@._V1_UY317_CR6,0,214,317_AL_.jpg',
        'imdb_link': 'https://www.imdb.com/name/nm0005351/?ref_=tt_cl_t_1',
        'gender': 'Male',
        'age': 37,
        'seeking_roles': False,
        'seeking_description': ''
    }

    actor_update = {
        'age': 38
    }

    new_movie = {
        'title': 'Deadpool',
        'image_link': 'https://m.media-amazon.com/images/M/MV5BYzE5MjY1ZDgtMTkyNC00MTMyLThhMjAtZGI5OTE1NzFlZGJjXkEyXkFqcGdeQXVyNjU0OTQ0OTY@._V1_FMjpg_UX1000_.jpg',
        'imdb_link': 'https://www.imdb.com/title/tt1431045/?ref_=fn_al_tt_1',
        'release_date': '2016-02-14',
        'seeking_talent': False,
        'seeking_description': ''
    }

    movie_update = {
        'seeking_talent': True
    }

    actor_search = {
        'search_term': 'reynolds'
    }

    movie_search = {
        'search_term': 'dead'
    }

    bad_search = {
        'search_term': 'aaabhghagb'
    }

    def setUp(self):
        """ Define test variables """

        """ Initialize the API App """
        self.app = create_app()
        self.client = self.app.test_client
        self.database_path = TEST_DB_PATH
        setup_db(self.app, self.database_path)

        # bind app to current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
    

    
    def test_get_success_actors(self):
        print(""" Test GET /actors success """)
        res = self.client().get('/actors')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(len(data['actors']), 0)
    
    def test_404_get_actor(self):
        print(""" Test GET /actors/1245 404 failure """)
        res = self.client().get('/actors/1245')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')
    
    def test_create_actor_success(self):
        print("""Test POST /actors add success """)
        res = self.client().post('/actors', json=self.new_actor)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['id'])
        self.__class__.new_actor_id = data['id']
    
    def test_400_create_actor(self):
        print("""Test POST /actors 400 failure """)
        res = self.client().post('/actors', json=None)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'bad request')
    
    def test_422_create_actor(self):
        print("""Test POST /actors 422 failure """)
        res = self.client().post('/actors', json=self.new_movie)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'unprocessable')
    
    def test_405_patch_actor(self):
        print("""Test PATCH /actors 405 failure """)
        res = self.client().patch('/actors', json=self.new_actor)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 405)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'method not allowed')
    
    def test_404_patch_actor(self):
        print("""Test PATCH /actors/<id> 404 failure """)
        res = self.client().patch('/actors/1245', json=self.actor_update)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')

    def test_422_patch_actor(self):
        print("""Test PATCH /actors/<id> 422 failure """)
        res = self.client().patch('/actors/' + str(self.__class__.new_actor_id), json=None)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'unprocessable')
    
    def test_patch_actor_success(self):
        print("""Test PATCH /actors/<id> success """)
        res = self.client().patch('/actors/' + str(self.__class__.new_actor_id), json=self.actor_update)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['actor'])

    def test_404_get_actor_details(self):
        print("""Test GET /actors/<id> 404 failure """)
        res = self.client().get('/actors/1245')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found') 
    
    def test_get_actor_details_success(self):
        print("""Test GET /actors/<id> success """)
        res = self.client().get('/actors/' + str(self.__class__.new_actor_id))
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['actor'])
    
    def test_404_delete_actor(self):
        print("""Test DELETE /actors/<id> 404 failure """)
        res = self.client().delete('/actors/1245')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')
    
    def test_delete_actor_success(self):
        print("""Test DELETE /actors/<id> success """)
        res = self.client().delete('/actors/' + str(self.__class__.new_actor_id))
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['id'], self.__class__.new_actor_id)

    def test_422_search_actor(self):
        print("""Test POST /actors/search 422 failure """)
        res = self.client().post('/actors/search', json=None)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'unprocessable')
    
    def test_bad_search_actor(self):
        print("""Test POST /actors/search empty search """)
        res = self.client().post('/actors/search', json=self.bad_search)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['count'], 0) 
        self.assertEqual(len(data['actors']), 0)
    
    def test_search_actor(self):
        print("""Test POST /actors/search search success """)
        res = self.client().post('/actors/search', json=self.actor_search)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['count'], 1) 
        self.assertEqual(len(data['actors']), 1)      

    def test_get_success_movies(self):
        print(""" Test GET /movies success """)
        res = self.client().get('/movies')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(len(data['movies']), 0)
    
    def test_404_get_movie(self):
        print(""" Test GET /movies/1245 404 failure """)
        res = self.client().get('/movies/1245')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')
    
    def test_create_movie_success(self):
        print("""Test POST /movies add success """)
        res = self.client().post('/movies', json=self.new_movie)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['id'])
        self.__class__.new_movie_id = data['id']
    
    def test_400_create_movie(self):
        print("""Test POST /movies 400 failure """)
        res = self.client().post('/movies', json=None)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'bad request')
    
    def test_422_create_movie(self):
        print("""Test POST /movies 422 failure """)
        res = self.client().post('/movies', json=self.new_actor)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'unprocessable')

    def test_405_patch_movie(self):
        print("""Test PATCH /movies 405 failure """)
        res = self.client().patch('/movies', json=self.new_movie)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 405)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'method not allowed')
    
    def test_404_patch_movie(self):
        print("""Test PATCH /movies/<id> 404 failure """)
        res = self.client().patch('/movies/1245', json=self.movie_update)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')

    def test_422_patch_movie(self):
        print("""Test PATCH /movies/<id> 422 failure """)
        res = self.client().patch('/movies/' + str(self.__class__.new_movie_id), json=None)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'unprocessable')

    def test_patch_movie_success(self):
        print("""Test PATCH /movies/<id> success """)
        res = self.client().patch('/movies/' + str(self.__class__.new_movie_id), json=self.movie_update)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['movie'])

    def test_404_get_movie_details(self):
        print("""Test GET /movies/<id> 404 failure """)
        res = self.client().get('/movies/1245')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found') 
    
    def test_get_movie_details_success(self):
        print("""Test GET /actors/<id> success """)
        res = self.client().get('/movies/' + str(self.__class__.new_movie_id))
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['movie'])

    def test_404_delete_movie(self):
        print("""Test DELETE /movies/<id> 404 failure """)
        res = self.client().delete('/movies/1245')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')
    
    def test_delete_movie_success(self):
        print("""Test DELETE /movies/<id> success """)
        res = self.client().delete('/movies/' + str(self.__class__.new_movie_id))
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['id'], self.__class__.new_movie_id)

    def test_422_search_movie(self):
        print("""Test POST /movies/search 422 failure """)
        res = self.client().post('/movies/search', json=None)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'unprocessable')
    
    def test_bad_search_movie(self):
        print("""Test POST /movies/search empty search """)
        res = self.client().post('/movies/search', json=self.bad_search)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['count'], 0) 
        self.assertEqual(len(data['movies']), 0)
    
    def test_search_movie(self):
        print("""Test POST /movies/search search success """)
        res = self.client().post('/movies/search', json=self.movie_search)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['count'], 1) 
        self.assertEqual(len(data['movies']), 1)

    def test_get_movies_for_actor_no_results(self):
        print(""" Test GET /castlist/actors/<actor_id> no results """)
        res = self.client().get('/castlist/actors/1245')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['count'], 0)
        self.assertEqual(len(data['movies']), 0)

    def test_get_movies_for_actor(self):
        print(""" Test GET /castlist/actors/<actor_id> results """)
        res = self.client().get('/castlist/actors/' + str(self.__class__.new_actor_id))
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['count'], 1)
        self.assertEqual(len(data['movies']), 1)

    def test_get_actors_for_movie_no_results(self):
        print(""" Test GET /castlist/movies/<movie_id> no results """)
        res = self.client().get('/castlist/movies/1245')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['count'], 0)
        self.assertEqual(len(data['actors']), 0)

    def test_get_actors_for_movie(self):
        print(""" Test GET /castlist/movies/<movie_id> results """)
        res = self.client().get('/castlist/movies/' + str(self.__class__.new_movie_id))
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['count'], 1)
        self.assertEqual(len(data['actors']), 1)

    def test_create_castlist_success(self):
        print("""Test POST /castlist add success """)
        res = self.client().post('/castlist', json={
         'movie_id': self.__class__.new_movie_id, 
         'actor_id': self.__class__.new_actor_id})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
    
    def test_400_create_castlist(self):
        print("""Test POST /castlist 400 failure """)
        res = self.client().post('/castlist', json=None)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'bad request')
    
    def test_422_create_castlist(self):
        print("""Test POST /castlist 422 failure """)
        res = self.client().post('/castlist', json={
         'movie_id': self.__class__.new_movie_id, 
         'actor_id': self.__class__.new_actor_id})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'unprocessable')
    
    def test_400_delete_castlist(self):       
        print(""" Test DELETE /castlist 400 failure """)
        res = self.client().delete('/castlist', json=None)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'bad request')
    
    def test_404_delete_castlist(self):       
        print(""" Test DELETE /castlist 404 failure """)
        res = self.client().delete('/castlist', json={'movie_id': 1245, 'actor_id': 1245})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')
    
    def test_delete_castlist_success(self):       
        print(""" Test DELETE /castlist success """)
        res = self.client().delete('/castlist', json={'movie_id': self.__class__.new_movie_id, 'actor_id': self.__class__.new_actor_id})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['id'])

def suite():
    suite = unittest.TestSuite()
    """ Actor Section """
    suite.addTest(SpotlightTests('test_get_success_actors'))
    suite.addTest(SpotlightTests('test_404_get_actor'))
    suite.addTest(SpotlightTests('test_create_actor_success'))
    suite.addTest(SpotlightTests('test_400_create_actor'))
    suite.addTest(SpotlightTests('test_422_create_actor'))
    suite.addTest(SpotlightTests('test_405_patch_actor'))
    suite.addTest(SpotlightTests('test_404_patch_actor'))
    suite.addTest(SpotlightTests('test_422_patch_actor'))
    suite.addTest(SpotlightTests('test_patch_actor_success'))
    suite.addTest(SpotlightTests('test_404_get_actor_details'))
    suite.addTest(SpotlightTests('test_get_actor_details_success'))
    suite.addTest(SpotlightTests('test_404_delete_actor'))
    suite.addTest(SpotlightTests('test_422_search_actor'))
    suite.addTest(SpotlightTests('test_bad_search_actor'))
    suite.addTest(SpotlightTests('test_search_actor'))

    """ Movie Section """
    suite.addTest(SpotlightTests('test_get_success_movies'))
    suite.addTest(SpotlightTests('test_404_get_movie'))
    suite.addTest(SpotlightTests('test_create_movie_success'))
    suite.addTest(SpotlightTests('test_400_create_movie'))
    suite.addTest(SpotlightTests('test_422_create_movie'))
    suite.addTest(SpotlightTests('test_405_patch_movie'))
    suite.addTest(SpotlightTests('test_404_patch_movie'))
    suite.addTest(SpotlightTests('test_422_patch_movie'))
    suite.addTest(SpotlightTests('test_patch_movie_success'))
    suite.addTest(SpotlightTests('test_404_get_movie_details'))
    suite.addTest(SpotlightTests('test_get_movie_details_success'))
    suite.addTest(SpotlightTests('test_404_delete_movie'))
    suite.addTest(SpotlightTests('test_422_search_movie'))
    suite.addTest(SpotlightTests('test_bad_search_movie'))
    suite.addTest(SpotlightTests('test_search_movie'))

    """ Castlist Section """
    suite.addTest(SpotlightTests('test_get_movies_for_actor_no_results'))
    suite.addTest(SpotlightTests('test_get_actors_for_movie_no_results'))
    suite.addTest(SpotlightTests('test_400_create_castlist'))
    suite.addTest(SpotlightTests('test_create_castlist_success'))
    suite.addTest(SpotlightTests('test_422_create_castlist'))
    suite.addTest(SpotlightTests('test_400_delete_castlist'))
    suite.addTest(SpotlightTests('test_404_delete_castlist'))
    suite.addTest(SpotlightTests('test_delete_castlist_success'))
    

    """ Cleanup Deletes """
    suite.addTest(SpotlightTests('test_delete_actor_success'))
    suite.addTest(SpotlightTests('test_delete_movie_success'))
    return suite

# Make tests executable
if __name__ == "__main__":
    runner = unittest.TextTestRunner()
    runner.run(suite())