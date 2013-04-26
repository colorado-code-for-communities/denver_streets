import unittest
import os, sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0,parent_dir)
import denver_streets

class DenverStreetsTestCase(unittest.TestCase):
    def setUp(self):
        # app.app.config['FLASK_ENV'] = 'test'
        denver_streets.database.init_db()

    def tearDown(self):
        denver_streets.database.drop_db()

    def test_root_index(self):
        ''

    def test_closure_index(self):
        ''

    def test_closure_by_date(self):
        ''

if __name__ == '__main__':
    unittest.main()
