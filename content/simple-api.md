Title: Auto-generated REST API for MS SQL database
Date: 2021-01-16 17:00
Category: Blog
Summary: Creating an automatic REST API with Flask and SQLSorcery for an MS SQL database.

## The Concept

Suppose you have a database with tables and views that you want to expose as JSON through
a REST API but you don't want to couple the database tables with object models in your
API but rather have it simply expose the data for querying (read-only). 

How could this be done easily and with minimal code?

## The Approach

[Flask](https://flask.palletsprojects.com/en/1.1.x/) has to be the simplest web app microframework
I've ever dealt with (though Node's [Express](https://expressjs.com/) and Ruby's 
[Sinatra](http://sinatrarb.com/) certainly come close). It has a great function `jsonify` that
makes it dead simple to serve a JSON response to a client request.

```python
# app.py
from flask import Flask, jsonify

app = Flask(__name__)

@app.route("/api/")
def index():
    data = {
        "name": "dchess",
        "text": "Hello, World",
    }
    return jsonify(data)
```

Spin it up on `localhost:5000/api/` and voila, data!

## Here comes the Sorcery

That's simple enough but how do we substitute the hard coded dictionary for a database query? This is
where [SQLAlchemy](https://www.sqlalchemy.org/) and [Pandas](https://pandas.pydata.org/) come in handy.

I almost always want to use these two packages together and so a while back I created a pypi package to
provide a simple facade with some syntactic sugar to make that even simpler called [SQLSorcery](https://sqlsorcery.readthedocs.io/en/latest/). It's built on top of both of them and has a simple way [to optionally install
database adapter packages](https://sqlsorcery.readthedocs.io/en/latest/cookbook/installation.html) like [pyodbc](https://pypi.org/project/pyodbc/). 

That allows me to easily pass in my database connection credentials with environment
variables and make sql queries using the Pandas `.read_sql_query()` method. 


## Environment

I'm a fan of [Pipenv](https://pipenv.pypa.io/en/latest/). It's so simple to install python package dependencies
into a local virtual environment and also handle environment variables from a `.env` file. Effectively combining
all the functionality of [pip](https://pypi.org/project/pip/), [venv](https://docs.python.org/3/tutorial/venv.html), and [python-dotenv](https://saurabh-kumar.com/python-dotenv/). 

```
$ pipenv install Flask, sqlsorcery[mssql]
```

And just like that we're ready to develop.

Let's add some environment variables to a `.env` file to start:

```
DB_SERVER=
DB=
DB_SCHEMA=
DB_USER=
DB_PWD=

FLASK_APP=app.py
```

## Querying our Data

Then we can return data from a table as simple as:

```python
from sqlsorcery import MSSQL
import pandas as pd

db = MSSQL()

data = pd.read_sql_table("your_table_name", con=db.engine, schema=db.schema)
```

It's that simple!

To quickly convert that dataframe into a list of dictionaries (to return as JSON), we
can use the Pandas `to_dict()` method.

```python
data = data.to_dict(orient="records")
```

What if we want to list all the tables in our database schema? Simple!

```python
tables = db.engine.table_names(schema=db.schema)
```

With those two approaches and Flask's `jsonify` we have everything we need to make a quick,
easy, and minimal API on top of any tables in our database schema.

## A User Interface

While we can create an API for machines to read from, it'd be nice to have at least an index of
tables that a human can read, navigate, and learn what data exists before pointing tools like [curl](https://curl.se/), 
[postman](https://www.postman.com/), or [Requests](https://requests.readthedocs.io/en/master/) at it. 

No worries! A tiny [jinja](https://jinja.palletsprojects.com/en/2.11.x/) HTML template should suffice for a quick list of table names linked to their api endpoint will be just minimal enough to work!

```html
# templates/index.html
<ul>
    {% for table in tables %}
    <li><a href="/api/{{ table}}">{{ table }}</a></li>
    {% endfor %}
</ul>
```

## Putting it all together

At this point we should have a file directory that looks like this:

```bash
.
├── Pipfile
├── .env
├── app.py
└── templates
    └── index.html
```

Let's finish off our `app.py` and give it a test run:

```python
# app.py

from flask import Flask, jsonify, render_template
from sqlsorcery import MSSQL
import pandas as pd

app = Flask(__name__)
db = MSSQL()


@app.route("/api")
def index():
    tables = db.engine.table_names(schema=db.schema)
    return render_template("index.html", tables=tables)


@app.route("/api/<table>", methods=["GET"])
def endpoint(table):
    data = pd.read_sql_table(table, con=db.engine, schema=db.schema)
    data = data.to_dict(orient="records")
    return jsonify(data)
```

Spin it up on [localhost:5000/api/](localhost:5000/api/) and explore your data!

```
$ pipenv run flask run
```


## Conclusion

I wouldn't take this and deploy it to production anywhere without some serious security
decisions, but it makes for a nice proof-of-concept. And certainly could be expanded to
include user authentication, a proper production server like [gunicorn](https://gunicorn.org/) and a nicer
user interface. But at point you might be better off with [Flask-API](https://www.flaskapi.org/) or 
[Django REST Framework](https://www.django-rest-framework.org/), both of which I've used with success. 

But still, not bad for less than 20 lines of code. 

All the code for this blog can be found on my [github](https://github.com/dchess/simple_api). 
Feel free to fork and use it however you like. 

SQLSorcery is also MIT licensed and free to use. It's in active development and contributors are welcome. 
