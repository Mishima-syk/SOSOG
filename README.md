# SOSOG
paper information sharing system

Standing on the shoulders of Giants (SOSOG).

## Install

    conda install -c anaconda flask
    conda install -c conda-forge flask-debugtoolbar
    conda install -c conda-forge flask-sqlalchemy

## Create database

    $ python
    >>> from app import db
    >>> db.create_all()

## Run app

    export FLASK_APP=app.py
    export FLASK_DEBUG=1
    flask run