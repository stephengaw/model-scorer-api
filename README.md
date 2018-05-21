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

#### Example

Request:

```
curl --request POST \
  --url http://127.0.0.1/register \
  --header 'content-type: application/json' \
  --data '{"username": "stephen", "password": "asdf"}'
```

Response:

```
{
    "message": "User created successfully."
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

#### Example

Request:

```
curl --request POST \
  --url http://{URL}/auth \
  --header 'content-type: application/json' \
  --data '{"username": "stephen", "password": "asdf"}'
```

Response:

```
{
    "access_token": "{JWT_TOKEN}"
}
```

### GET /scorers

List the descriptions of all the scorers that are uploaded, and can be scored against.

#### Example

Request:

```
curl --request GET \
  --url http://{URL}/scorers
```

Response:

```
{
    "scorers": [
        {
            "scorer_id": "model2",
            "scorer_summary": "DecisionTreeClassifier(class_weight=None, criterion='gini', max_depth=None,\n            max_features=None, max_leaf_nodes=None,\n            min_impurity_decrease=0.0, min_impurity_split=None,\n            min_samples_leaf=1, min_samples_split=2,\n            min_weight_fraction_leaf=0.0, presort=False, random_state=None,\n            splitter='best')",
            "scorer_uploaded": null
        },
        {
            "scorer_id": "model3",
            "scorer_summary": "RandomForestClassifier(bootstrap=True, class_weight=None, criterion='gini',\n            max_depth=None, max_features='auto', max_leaf_nodes=None,\n            min_impurity_decrease=0.0, min_impurity_split=None,\n            min_samples_leaf=1, min_samples_split=2,\n            min_weight_fraction_leaf=0.0, n_estimators=10, n_jobs=1,\n            oob_score=False, random_state=None, verbose=0,\n            warm_start=False)",
            "scorer_uploaded": null
        }
    ]
}
```

### GET /scorers/{scorer_id}

View the description of the specific scorer, `scorer_id`

### POST /scorers/{scorer_id}

Upload a new scorer, to be identified by the unique `scorer_id`. The scorer 
must be in the form of a `dill` serialised python object.

#### Headers

* Authorization   JWT {{jwt_token}}

#### Body

Binary

The `dill` serialised `sklearn` fitted model object.

#### Example

Request:

```
curl --request POST \
  --url http://{URL}/scorers/model3 \
  --header 'authorization: JWT {JWT_TOKEN}' \
  --data-binary "@test-examples/iris_rf_model.pkl"
```

Response:

```
{
    "scorers": [
        {
            "scorer_id": "model2",
            "scorer_summary": "DecisionTreeClassifier(class_weight=None, criterion='gini', max_depth=None,\n            max_features=None, max_leaf_nodes=None,\n            min_impurity_decrease=0.0, min_impurity_split=None,\n            min_samples_leaf=1, min_samples_split=2,\n            min_weight_fraction_leaf=0.0, presort=False, random_state=None,\n            splitter='best')",
            "scorer_uploaded": null
        },
        {
            "scorer_id": "model3",
            "scorer_summary": "RandomForestClassifier(bootstrap=True, class_weight=None, criterion='gini',\n            max_depth=None, max_features='auto', max_leaf_nodes=None,\n            min_impurity_decrease=0.0, min_impurity_split=None,\n            min_samples_leaf=1, min_samples_split=2,\n            min_weight_fraction_leaf=0.0, n_estimators=10, n_jobs=1,\n            oob_score=False, random_state=None, verbose=0,\n            warm_start=False)",
            "scorer_uploaded": null
        }
    ]
}
```

### DELETE /scorers/{scorer_id}

Remove the specific scorer, identified by `scorer_id`.

#### Headers

* Authorization   JWT {{jwt_token}}

### PUT /scorers/{scorer_id}

Update the specific scorer, identified by `scorer_id`. If the scorer does not 
already exist, create a new scorer, with that `scorer_id`. 

#### Headers

* Authorization   JWT {{jwt_token}}

#### Body

Binary

The `dill` serialised `sklearn` fitted model object.

### POST /scorers/{scorer_id}/predict/dict

Use the scorer, identified by `scorer_id`, to make predictions (using the sklearn 
model objects `.predict()` method) on the new data.
The new data is in the form of a python dict structure, which will be converted 
into a pandas dataframe for use with the sklearn model.

#### Headers

* Content-Type application/json
* Authorization   JWT {{jwt_token}}

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

* Content-Type application/json
* Authorization   JWT {{jwt_token}}

#### Body

```json
{
	"features": [1.0,1.0,3.0,2.0]
}
```

#### Example

```bash
curl --request POST \
  --url http://{URL}/scorers/model3/predict/list \
  --header 'authorization: JWT {JWT_TOKEN}' \
  --header 'content-type: application/json' \
  --data '{"features": [1.0,1.0,3.0,2.0]}'
```

### POST /scorers/{scorer_id}/transform/dict

Use the scorer, identified by `scorer_id`, to make predictions (using the sklearn 
model objects `.transform()` method) on the new data.
The new data is in the form of a python dict structure, which will be converted 
into a pandas dataframe for use with the sklearn model.

#### Headers

* Content-Type application/json
* Authorization   JWT {{jwt_token}}


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

