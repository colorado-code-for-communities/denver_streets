import unittest
import json, os
import importer

# read_closures() should return import_test_fixtures.txt
fixtures_dir = os.getcwd() + "/tests/fixtures"

class ImporterTests(unittest.TestCase):
    def setUp(self):
        self.closure_json = open(fixtures_dir + '/importer_test_fixtures.txt')

    def testImportClosure(self):
        importer.import_closures()
        assert(true).equals(true)
        #assert(Clo

if __name__ == '__main__':
    unittest.main()
