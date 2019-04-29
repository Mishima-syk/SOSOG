# SOSOG
Reference information sharing system

Standing on the shoulders of Giants (SOSOG).

## Install

    conda install -c anaconda flask
    conda install -c conda-forge flask-debugtoolbar
    conda install -c conda-forge flask-sqlalchemy
    # for tests
    conda install -c anaconda nose

## Create database

    $ python
    >>> from app import db
    >>> db.create_all()

## Run app

    export FLASK_APP=app.py
    export FLASK_DEBUG=1
    flask run 
    # and then, access http://localhost:5000/