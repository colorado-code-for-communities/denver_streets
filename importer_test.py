import app
import unittest
import json, os
from lib import importer

fixtures_dir = os.getcwd() + "/tests/fixtures"
database = app.database
models = app.models

class ImporterTests(unittest.TestCase):
    def setUp(self):
        # set up test db
        self.closure_json = json.loads(open(fixtures_dir + '/importer_test_fixtures.txt').read())
        database.init_db()

    def tearDown(self):
        database.drop_db()

    def testImportClosure(self):
        self.setUp()
        importer.import_closures()
        self.assertEquals(len(database.session.query(models.Closure).all()), 6)
        self.tearDown()

if __name__ == '__main__':
    unittest.main()
