import unittest
import json, os
import database_test
from lib import importer

# read_closures() should return import_test_fixtures.txt
fixtures_dir = os.getcwd() + "/tests/fixtures"

class ImporterTests(unittest.TestCase):
    def setUp(self):
        # set up test db
        self.closure_json = json.loads(open(fixtures_dir + '/importer_test_fixtures.txt').read())
        database_test.init_db()

    def tearDown(self):
        database_test.drop_db()

    def testImportClosure(self):
        importer.import_closures()
        assert(true).equals(true)

if __name__ == '__main__':
    unittest.main()
