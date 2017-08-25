import os
import sys
import unittest
rootdir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, rootdir)
from app import db, User, Bookmark, Reference, Tag


class TestUser(unittest.TestCase):

    def setUp(self):
        dbfile = os.path.join(rootdir, "sosog.db")
        if os.path.exists(dbfile):
            os.unlink(dbfile)
            print "Delete DBFILE"
        db.create_all()
        print "Create DBFILE"
        
    def test_user_add(self):
        u = User("testuser", "test@example.com", "test1234")
        db.session.add(u)
        db.session.commit()
        self.assertEqual(u.id, 1)

    def test_ref_add(self):
        pass
