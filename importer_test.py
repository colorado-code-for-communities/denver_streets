import unittest
import json, os
import database_test
from lib import importer
import models

# read_closures() should return import_test_fixtures.txt
fixtures_dir = os.getcwd() + "/tests/fixtures"

class ImporterTests(unittest.TestCase):
    def setUp(self):
        # set up test db
        self.closure_json = json.loads(open(fixtures_dir + '/importer_test_fixtures.txt').read())
        database_test.init_db()

    def tearDown(self):
        database_test.destroy_db()

    def testImportClosure(self):
        importer.import_closures()
        self.assertEquals(len(database_test.session.query(models.Closure).all()), 6)

if __name__ == '__main__':
    unittest.main()
