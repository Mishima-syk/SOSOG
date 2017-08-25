# -*- coding: utf-8 -*-

from flask import Flask, request, session, redirect, url_for, abort, render_template, flash, jsonify, make_response
from flask_debugtoolbar import DebugToolbarExtension
from flask_sqlalchemy import SQLAlchemy
import os

# flask settings
DEBUG = True
SECRET_KEY = 'Standing on the shoulders of Giants'
databese_file = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'sosog.db')
SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_DATABASE_URI = 'sqlite:///%s' % databese_file

# application
app = Flask(__name__)
app.config.from_object(__name__)

# database settings
db = SQLAlchemy(app)

toolbar = DebugToolbarExtension(app)


bookmark_tag = db.Table('bookmark_tag',
                        db.Column('bookmark_id', db.Integer, db.ForeignKey('bookmark.id')),
                        db.Column('tag_id', db.Integer, db.ForeignKey('tag.id'))
                        )


class Bookmark(db.Model):
    __tablename__ = 'bookmark'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    reference_id = db.Column(db.Integer, db.ForeignKey('reference.id'))
    description = db.Column(db.Text())
    user = db.relationship('User', back_populates="references")
    reference = db.relationship("Reference", back_populates="users")
    tags = db.relationship("Tag", secondary=bookmark_tag)


class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True)
    email = db.Column(db.String, unique=True)
    password = db.Column(db.String)
    authenticated = db.Column(db.Boolean, default=False)
    references = db.relationship("Bookmark", back_populates="user")

    def __init__(self, name, email, password):
        self.name = name
        self.email = email
        self.password = password

    def is_active(self):
        """True, as all users are active."""
        return True

    def get_id(self):
        """Return the email address to satisfy Flask-Login's requirements."""
        return self.email

    def is_authenticated(self):
        """Return True if the user is authenticated."""
        return self.authenticated

    def is_anonymous(self):
        """False, as anonymous users aren't supported."""
        return False


class Reference(db.Model):
    __tablename__ = 'reference'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(256), unique=True)
    description = db.Column(db.Text())
    pubmed_id = db.Column(db.String(10))
    doi = db.Column(db.String(256))
    arxiv_id = db.Column(db.String(256))
    usercount = db.Column(db.Integer)
    users = db.relationship("Bookmark", back_populates="reference")


class Tag(db.Model):
    __tablename__ = 'tag'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), unique=True)
    bookmarks = db.relationship("Bookmark", secondary=bookmark_tag)

    def __init__(self, name):
        self.name = name


@app.route('/')
def show_index():
    return "show index"


if __name__ == '__main__':
    app.run()
