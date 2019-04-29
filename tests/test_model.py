import os
import sys
import unittest
rootdir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, rootdir)
from app import db, User, Bookmark, Reference, Tag


class TestUser(unittest.TestCase):

    def tearDown(self):
        User.query.delete()

    def test_adduser(self):
        u = User("testuser", "test@example.com", "test1234")
        db.session.add(u)
        db.session.commit()
        self.assertEqual(u.id, 1)

        u2 = User("testuser2", "test2@example.com", "test1234")
        db.session.add(u2)
        db.session.commit()
        self.assertEqual(u2.id, 2)


class TestReference(unittest.TestCase):

    def tearDown(self):
        Reference.query.delete()
        db.session.commit()

    def test_reference_add(self):
        title = "Overexpression of Topoisomerase 2-Alpha Confers a Poor Prognosis in Pancreatic Adenocarcinoma Identified by Co-Expression Analysis."
        abstract = """In the significant module (R (2) = 0.30), a total of 20 network hub genes were identified, 6 of which were also hub nodes in the protein-protein interaction network of the module genes. In validation, TOP2A has a higher correlation than other hub genes. Also, in the test set (n = 118), TOP2A was more highly expressed in PDAC than normal pancreas samples (P < 0.001). What is more, gene set enrichment analysis demonstrated that eight gene sets (n = 118), "nucleotide excision repair," "P53 signaling pathway," "proteasome," "mismatch repair," "homologous recombination," "DNA replication," "cell cycle," and "base excision repair," were enriched (FDR < 0.05). In gene ontology analysis, TOP2A in the enriched set was associated with cell cycle and cell division. Furthermore, survival analysis indicated that higher expression of TOP2A resulted in the lower overall survival time as well as disease-free survival time."""
        pubmed_id = "28815403"
        doi = "10.1007/s10620-017-4718-4"
        r = Reference(title=title,
                      abstract=abstract,
                      pubmed_id=pubmed_id,
                      doi=doi)
        db.session.add(r)
        db.session.commit()
        self.assertEqual(r.id, 1)
        self.assertEqual(r.abstract, abstract)
        self.assertEqual(r.pubmed_id, pubmed_id)
        self.assertEqual(r.doi, doi)


class TestBookmark(unittest.TestCase):

    def tearDown(self):
        User.query.delete()
        Reference.query.delete()
        Bookmark.query.delete()
        db.session.commit()

    def test_bookmark(self):
        u = User("testuser", "test@example.com", "test1234")
        u2 = User("testuser2", "test2@example.com", "test1234")
        db.session.add(u)
        db.session.add(u2)
        title = "Overexpression of Topoisomerase 2-Alpha Confers a Poor Prognosis in Pancreatic Adenocarcinoma Identified by Co-Expression Analysis."
        abstract = "abstract"
        pubmed_id = "28815403"
        doi = "10.1007/s10620-017-4718-4"
        ref = Reference(title=title,
                        abstract=abstract,
                        pubmed_id=pubmed_id,
                        doi=doi)
        db.session.add(ref)
        db.session.commit()

        bookmark = Bookmark(comment="TOPII ref")
        bookmark.reference = ref
        bookmark.user = u
        db.session.add(bookmark)
        db.session.commit()

        self.assertEqual(len(u.bookmarks), 1)
        title2 = "another ref"
        abstract2 = "abstract"
        pubmed_id2 = "28815404"
        doi2 = "10.1007/s10620-037-4718-4"
        ref2 = Reference(title=title2,
                         abstract=abstract2,
                         pubmed_id=pubmed_id2,
                         doi=doi2)
        db.session.add(ref2)
        db.session.commit()
        bookmark2 = Bookmark(comment="another ref")
        bookmark2.user = u
        bookmark2.reference = ref2
        db.session.add(bookmark2)
        db.session.commit()
        self.assertEqual(len(u.bookmarks), 2)
        self.assertEqual(u.bookmarks[0].comment, "TOPII ref")
        self.assertEqual(u.bookmarks[1].comment, "another ref")

        bookmark3 = Bookmark(comment="another comment")
        bookmark3.user = u2
        bookmark3.reference = ref2
        db.session.add(bookmark3)
        db.session.commit()
        self.assertEqual(len(u2.bookmarks), 1)
        self.assertEqual(u2.bookmarks[0].comment, "another comment")
        self.assertEqual(len(ref.bookmarks), 1)
        self.assertEqual(len(ref2.bookmarks), 2)


class TestNewTag(unittest.TestCase):

    def tearDown(self):
        Tag.query.delete()
        db.session.commit()

    def test_new_tag(self):
        t = Tag("TOP2")
        db.session.add(t)
        db.session.commit()
        self.assertEqual(t.name, "TOP2")


class TestTagRelationship(unittest.TestCase):

    def setUp(self):
        u = User("testuser", "test@example.com", "test1234")
        db.session.add(u)
        self.u = u
        title = "Overexpression of Topoisomerase 2-Alpha Confers a Poor Prognosis in Pancreatic Adenocarcinoma Identified by Co-Expression Analysis."
        abstract = "abstract"
        pubmed_id = "28815403"
        doi = "10.1007/s10620-017-4718-4"
        ref = Reference(title=title,
                        abstract=abstract,
                        pubmed_id=pubmed_id,
                        doi=doi)
        db.session.add(ref)
        db.session.commit()
        self.r = ref

        bookmark = Bookmark(comment="TOPII ref")
        bookmark.reference = ref
        bookmark.user = u
        db.session.add(bookmark)
        db.session.commit()
        self.b = bookmark

    def tearDown(self):
        User.query.delete()
        Reference.query.delete()
        Bookmark.query.delete()
        Bookmark.query.delete()
        Tag.query.delete()
        db.session.commit()

    def test_add_tag(self):
        self.assertEqual(len(self.b.tags), 0)
        t = Tag("TOP2")
        db.session.add(t)
        db.session.commit()
        t2 = Tag("Cancer")
        db.session.add(t2)
        db.session.commit()
        self.b.tags.append(t)
        db.session.commit()
        self.assertEqual(len(self.b.tags), 1)
        self.b.tags.append(t2)
        db.session.commit()
        self.assertEqual(len(self.b.tags), 2)
