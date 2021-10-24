# Spotlight Casting Agency API Project

This project is a sample website for the Spotlight Casting Agency, used as a capstone project for the Udacity Fullstack WebDevelopment nanodegree. You can add actors and movies, and then cast actors in movies based on permission level. There are three RBAC on this API. Without permissions actors and movies are viewable. A casting assistant can add, delete, and modify actors, cast actors in movies, and modify movie details. A director can do all the previous as well as add and delete movies.

All backend code follows [PEP8 style guidelines](https://www.python.org/dev/peps/pep-0008/). 

## Getting Started

### Pre-requisites and Local Development 
Developers using this project should already have Python3, pip and node installed on their local machines.

#### Backend

From the backend folder run `pip install requirements.txt`. All required packages are included in the requirements file. 

To run the application run the following commands: 
```
export FLASK_APP=flaskr
export FLASK_ENV=development
flask run
```

These commands put the application in development and directs our application to use the `__init__.py` file in our flaskr folder. Working in development mode shows an interactive debugger in the console and restarts the server whenever changes are made. If running locally on Windows, look for the commands in the [Flask documentation](http://flask.pocoo.org/docs/1.0/tutorial/factory/).

The application is run on `http://127.0.0.1:5000/` by default and is a proxy in the frontend configuration. 

#### Frontend

From the frontend folder, run the following commands to start the client: 
```
npm install // only once to install dependencies
pip install -r requirements.txt // install required python dependencies
source env/Scripts/activate // activate env
python app.py // to start the app
```

By default, the frontend will run on localhost:8080. 

### Tests
In order to run tests navigate to the backend folder and run the following commands: 

```
python test_api.py
```

All tests are kept in that file and should be maintained as updates are made to app functionality. 

## API Reference

### Getting Started
- Base URL: At present this app can only be run locally and is not hosted as a base URL. The backend app is hosted at the default, `http://127.0.0.1:5000/`, which is set as a proxy in the frontend configuration. 
- Authentication: This version of the application requires permissions to access certain endpoints. Authentication is provided via Auth0 and there are two roles: Casting Director and Executive producer. Without permissions users can interact with all information in the app in a read-only state. Casting directors can add, edit, and delete actors as well as cast them in movies. Executive Producers can do everything Casting Directors can but can also add, edit, and delete movies as well as remove actors from castlists.

### Error Handling
Errors are returned as JSON objects in the following format:
```
{
    "success": False, 
    "error": 400,
    "message": "bad request"
}
```
The API will return four error types when requests fail:
- 400: Bad Request
- 401: Invalid authorization header
- 403: Not permitted access
- 404: Resource Not Found
- 405: Method not allowed
- 422: Not Processable 

### Endpoints 
#### GET /actors
- General:
    - Returns an array of actors in the database and a success message. Returns only the "short" representation including an actor ID and a name. 
    - Request Args: None
- Sample: `curl http://127.0.0.1:5000/actors`

``` {
  "actors": [
      {"id": 1, "name": "Ryan Reynolds},
      {"id": 2, "name": "Brie Larson"}
  ]
  "success": true
}
```

#### GET /actors/<int:actor_id>
- General:
    - Fetches details for a specific actor and a success code.
    - Request Args: actor_id - integer
- `curl http://127.0.0.1:5000/actors/1`
```
{
  "actor": {
      "id": 1,
      "name": "Ryan Reynolds",
      "gender": "Male",
      "age": 37,
      "image_link": "https://m.media-amazon.com/images/M/MV5BOTI3ODk1MTMyNV5BMl5BanBnXkFtZTcwNDEyNTE2Mg@@._V1_UY317_CR6,0,214,317_AL_.jpg",
      "imdb_link": "https://www.imdb.com/name/nm0005351/?ref_=tt_cl_t_1",
      "seeking_roles": False,
      "seeking_description": "Not currently seeking roles."
  }
  "success": true
}
```

### POST /actors/search
- General:
    - Sends a post request in order to get actors matching a specific search term. It returns an array of the short version of each actor as well as a count of matching actors.
    - Request Args: None
- Sample:
    - `curl http://127.0.0.1:5000/actors/search -X POST -H "Content-Type: application/json" -d '{'search_term': 'Ryan'}'`
```
{
  "actors": [
    {
      "id": 1,
      "name": "Ryan Reynolds"
    }
  ],
  "count": 1,
  "success": true
}
```

### POST /actors
- General:
    - Sends a post request in order to add a new actor to the database. If successful it will return the ID of the newly added actor.
    - Request Args: None
    - Authorization: requires token with the permission `post:actors`
- Sample:
    - `curl http://127.0.0.1:5000/actors -X POST -H "Content-Type: application/json" -H "Authorization: Bearer [token]" -d '{'name': 'Hugh Jackman', 'age': 53, 'image_link': 'url-for-image', 'imdb_link': 'url-for-imdb', 'gender': 'Male', 'seeking_roles': False, 'seeking_description': 'optional string description'}'`
```
{
  "id": 2,
  "success": true
}
```

### PATCH /actors/<int:actor_id>
- General:
    - Sends a patch request in order to update an actor with an associated ID in the database. All parameters are optional. If successful will return success and the short version of the actor.
    - Request Args: actor_id - integer
    - Authorization: requires token with the permission `patch:actors`
- Sample:
    - `curl http://127.0.0.1:5000/actors -X PATCH -H "Content-Type: application/json" -H "Authorization: Bearer [token]" -d '{'name': 'Hugh Jackman', 'age': 54, 'image_link': 'url-for-image', 'imdb_link': 'url-for-imdb', 'gender': 'Male', 'seeking_roles': False, 'seeking_description': 'optional string description'}'`
```
{
  "actor": {
    'name': 'Hugh Jackman',
    'id': 2
  },
  "success": true
}
```

### DELETE /actors/<int:actor_id>
- General:
    - Sends a delete request in order to delete an actor with an associated ID in the database. If successful will return success and the ID of the deleted actor.
    - Request Args: actor_id - integer
    - Authorization: requires token with the permission `delete:actors`
- Sample:
    - `curl http://127.0.0.1:5000/actors -X DELETE -H "Content-Type: application/json" -H "Authorization: Bearer [token]"`
```
{
  "id": 2,
  "success": true
}
```

#### GET /movies
- General:
    - Returns an array of movies in the database and a success message. 
    - Request Args: None
- Sample: `curl http://127.0.0.1:5000/movies`

``` 
{
    "movie": {
        "id": 1,
        "title": "Deadpool",
        "release_date": "2016-02-14",
        "seeking_talent": False,
        "seeking_description": "Not currently casting talent."
   }
  "success": true
}
```





