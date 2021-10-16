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
npm start 
```

By default, the frontend will run on localhost:3000. 

### Tests
In order to run tests navigate to the backend folder and run the following commands: 

```
python test_flaskr.py
```

All tests are kept in that file and should be maintained as updates are made to app functionality. 

## API Reference

### Getting Started
- Base URL: At present this app can only be run locally and is not hosted as a base URL. The backend app is hosted at the default, `http://127.0.0.1:5000/`, which is set as a proxy in the frontend configuration. 
- Authentication: This version of the application does not require authentication or API keys. 

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
    - Request Args: None
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
#### GET /movies
- General:
    - Returns an array of movies in the database and a success message. 
    - Request Args: None
- Sample: `curl http://127.0.0.1:5000/categories/1/questions`

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

#### DELETE /questions/{question_id}
- General:
    - Deletes the question of the given ID if it exists. Returns appropriate HTTP status code and the ID of the question deleted.
    - Request Args: question id - integer
- `curl -X DELETE http://127.0.0.1:5000/questions/21`
```
{
  "success": true,
  "id": 21
}
```
#### POST /quizzes
- General:
    - Sends a post request in order to get the next quiz question.
    - Request Args: None 
- `curl http://127.0.0.1:5000/quizzes -X POST -H "Content-Type: application/json" -d '{"previous_questions": [20], "quiz_category": {"type": "Science", "id": "1"}}'`
```
{
  "question":
    {
      "id": "Hematology is a branch of medicine involving the study of what?",
      "question": 22,
      "answer": "Blood",
      "difficulty": 4,
      "category": "1"
    },
  "success": true,
}
```

#### POST /questions
- General:
    - Sends a post request in order to add a new question.
    - Request Args: None 
- `curl http://127.0.0.1:5000/questions -X POST -H "Content-Type: application/json" -d '{"question": "This is a new question", "answer": "This is a new answer", "difficulty": 1, "category", 1}'`
```
{
  "success": true,
}
```

#### POST /questions
- General:
    - Sends a post request in order to search for a list of questions matching a term.
    - Request Args: None 
- `curl http://127.0.0.1:5000/questions -X POST -H "Content-Type: application/json" -d '{"searchTerm": "aut"}'`
```
{
   "questions": [
    {
      "answer": "Tom Cruise",
      "category": 5,
      "difficulty": 4,
      "id": 4,
      "question": "What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?"
    },
    {
      "answer": "Maya Angelou",
      "category": 4,
      "difficulty": 2,
      "id": 5,
      "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
    }
  ],
  "totalQuestions": 2,
  "currentCategory": "",
  "success": true
}
```



