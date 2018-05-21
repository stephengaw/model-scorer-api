# Model Scoring API

REST API to scored trained scikit-learn models ("scorers"), and then score unless
 data against these models.
 
## Endpoints

### POST /register

Register a new user with username and password

#### Headers

Content-Type application/json

#### Body

```json
{
	"username": "stephen",
	"password": "asdf"
}
```

### POST /auth

Authenticate a user with username and password, generating a JWT.

#### Headers

Content-Type application/json

#### Body

```json
{
	"username": "stephen",
	"password": "asdf"
}
```

### GET /scorers

List the descriptions of all the scorers that are uploaded, and can be scored against.


### GET /scorers/{scorer_id}

View the description of the specific scorer, `scorer_id`

### POST /scorers/{scorer_id}

Upload a new scorer, to be identified by the unique `scorer_id`. The scorer 
must be in the form of a `dill` serialised python object.

#### Headers

Authorization   JWT {{jwt_token}}

#### Body

Binary

The `dill` serialised `sklearn` fitted model object.

### DELETE /scorers/{scorer_id}

Remove the specific scorer, identified by `scorer_id`.

#### Headers

Authorization   JWT {{jwt_token}}


### PUT /scorers/{scorer_id}

Update the specific scorer, identified by `scorer_id`. If the scorer does not 
already exist, create a new scorer, with that `scorer_id`. 

#### Headers

Authorization   JWT {{jwt_token}}

#### Body

Binary

The `dill` serialised `sklearn` fitted model object.

### POST /scorers/{scorer_id}/predict/dict

Use the scorer, identified by `scorer_id`, to make predictions (using the sklearn 
model objects `.predict()` method) on the new data.
The new data is in the form of a python dict structure, which will be converted 
into a pandas dataframe for use with the sklearn model.


#### Headers

Content-Type application/json

#### Body

```json
{
	"features": {
		"Unnamed: 0": [5406],
		"full_description": ["Train <= 50 km 7% VRS Wochenticket:08.12-14.12.2014"],
		"amount": [29.1999], 
		"Claim_type_receipt": [1],
		"Multi_day_flag": [0], 
		"France": [0],
		"Germany": [1],
		"India": [0], 
		"Italy": [0], 
		"Netherlands": [0],
		"Other": [0], 
		"Spain": [0], 
		"United States of America": [0], 
		"null": [0]
	}
}
```

### POST /scorers/{scorer_id}/predict/list

Use the scorer, identified by `scorer_id`, to make predictions (using the sklearn 
model objects `.predict()` method) on the new data.
The new data is in the form of a list, which will be converted into a numpy 1D
array for use with the sklearn model.

#### Headers

Content-Type application/json

#### Body

```json
{
	"features": [1.0,1.0,3.0,2.0]
}
```

### POST /scorers/{scorer_id}/transform/dict

Use the scorer, identified by `scorer_id`, to make predictions (using the sklearn 
model objects `.transform()` method) on the new data.
The new data is in the form of a python dict structure, which will be converted 
into a pandas dataframe for use with the sklearn model.

#### Headers

Content-Type application/json

#### Body

```json
{
	"features": {
		"Unnamed: 0": [5406],
		"full_description": ["Train <= 50 km 7% VRS Wochenticket:08.12-14.12.2014"],
		"amount": [29.1999], 
		"Claim_type_receipt": [1],
		"Multi_day_flag": [0], 
		"France": [0],
		"Germany": [1],
		"India": [0], 
		"Italy": [0], 
		"Netherlands": [0],
		"Other": [0], 
		"Spain": [0], 
		"United States of America": [0], 
		"null": [0]
	}
}
```

## Run

### Local Python Installation with Flask Web Server

Ensure the `data.db` SQLite database already exists. 

```bash
python app.py
```

Ensure running at the default URL: <http://localhost:5001/scorers>

### Local Python Installation using uWSGI

This method will automatically create the `data.db` SQLite database if it does 
not already exists.

```
uwsgi uwsgi-local.ini
```

Ensure running at the default URL: <http://localhost:5001/scorers>

### Dockerised App with NginX and uWSGI

#### Build Image

```bash
docker build -t model-scorer-api .
```

#### Run Container

```bash
docker run -p 80:80 --name model-scorer-api model-scorer-api
```

<http://localhost/scorers>

## Known Issues/Further Development

* Hash passwords in database.
* Use external database for persistence.
* Disable open registration of users, configure an admin user and only allow 
the admin to register new users.
* Unsure if Nginx should be in the same container as the flask app running 
 with uWSGI. Would it be better to refactor into seperate orchestrated container
 services?
* Better dill pickled data validation on upload of a new scorer model.
* Load scorer models from a location on the file system for automatic 
deployment.

