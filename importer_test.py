import unittest
import json, os
from lib import importer

# read_closures() should return import_test_fixtures.txt
fixtures_dir = os.getcwd() + "/tests/fixtures"

class ImporterTests(unittest.TestCase):
    def setUp(self):
        self.closure_json = json.loads(open(fixtures_dir + '/importer_test_fixtures.txt').read())

    def testImportClosure(self):
        print self.closure_json
        importer.import_closures()
        assert(true).equals(true)
        #assert(Clo

if __name__ == '__main__':
    unittest.main()
