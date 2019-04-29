# -*- coding: utf-8 -*-

from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

bookmarks_tags = db.Table('bookmark_tag',
                        db.Column('bookmark_id', db.Integer, db.ForeignKey('bookmark.id')),
                        db.Column('tag_id', db.Integer, db.ForeignKey('tag.id'))
                        )

bookmarks_users = db.Table('bookmarks_users',
                        db.Column('bookmark_id', db.Integer, db.ForeignKey('bookmark.id')),
                        db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
                        db.Column('is_read', db.Boolean)
                        )

class Bookmark(db.Model):
    __tablename__ = 'bookmark'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    reference_id = db.Column(db.Integer, db.ForeignKey('reference.id'))
    comment = db.Column(db.Text())
    unread = db.Column(db.Boolean)
    star = db.Column(db.Boolean)
    reference = db.relationship("Reference", back_populates="users")
    users = db.relationship('User', secondary=bookmarks_users, back_populates="user_bookmarts")
    tags = db.relationship("Tag", secondary=bookmarks_tags, back_populates="tag_bookmarks")

    def __init__(self, comment):
        self.comment = comment


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
    abstract = db.Column(db.Text())
    pubmed_id = db.Column(db.String(10))
    doi = db.Column(db.String(256))
    arxiv_id = db.Column(db.String(256))
    starcount = db.Column(db.Integer, default=0)
    users = db.relationship("Bookmark", back_populates="reference")

    def __init__(self, **k):
        self.title = k.get("title", "Title not found")
        self.abstract = k.get("abstract", "abstract not found")
        self.pubmed_id = k.get("pubmed_id", None)
        self.doi = k.get("doi", None)
        self.arxiv_id = k.get("arxiv_id", None)


class Tag(db.Model):
    __tablename__ = 'tag'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), unique=True)


    def __init__(self, name):
        self.name = name


