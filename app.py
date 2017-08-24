# -*- coding: utf-8 -*-

from flask import Flask, request, session, redirect, url_for, abort, render_template, flash, jsonify, make_response
from flask_debugtoolbar import DebugToolbarExtension
from flask_sqlalchemy import SQLAlchemy
import os

# flask settings
DEBUG = True
SECRET_KEY = 'Standing on the shoulders of Giants'
databese_file = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'sosog.db')
SQLALCHEMY_DATABASE_URI = 'sqlite:///%s' % databese_file

# application
app = Flask(__name__)
app.config.from_object(__name__)

# database settings
db = SQLAlchemy(app)

toolbar = DebugToolbarExtension(app)


@app.route('/')
def show_index():
    return "show index"


if __name__ == '__main__':
    app.run()
