import os
import sys
import unittest
rootdir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, rootdir)
from app import db

dbfile = os.path.join(rootdir, "sosog.db")
if os.path.exists(dbfile):
    os.unlink(dbfile)
    print("Delete DBFILE")
db.create_all()
print("Create DBFILE")
