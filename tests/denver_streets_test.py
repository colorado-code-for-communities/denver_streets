from test_helpers import *

database = denver_streets.database

class DenverStreetsTestCase(unittest.TestCase):
    def setUp(self):
        # app.app.config['FLASK_ENV'] = 'test'
        self.closure_json = open(fixtures_dir + '/importer_test_fixtures.txt').read()
        self.app = denver_streets.app.test_client()
        database.init_db()
        importer.import_closures(self.closure_json)

    def tearDown(self):
        denver_streets.database.drop_db()

    def test_root_index(self):
        result = self.app.get('/')
        assert json.loads(result.data)['items'][0]['closures_href'] == '/closures'

    def test_closure_index(self):
        result = self.app.get('/closures')
        closures = json.loads(result.data)['items']
        assert len(closures) == 6

    def test_closure_by_date(self):
        ''

if __name__ == '__main__':
    unittest.main()
