from test_helpers import *

database = denver_streets.database

# Set datetime.now and datetime.today to April 26, 2013 in some tests
class Today(datetime.date):
    @classmethod
    def now(cls):
        return cls(2013, 4, 26)

class DenverStreetsTestCase(unittest.TestCase):
    def setUp(self):
        self.closure_json = open(fixtures_dir + '/importer_test_fixtures.txt').read()
        self.app = denver_streets.app.test_client()
        database.init_db()
        importer.import_closings(self.closure_json)

    def tearDown(self):
        denver_streets.database.drop_db()

    def test_root_index(self):
        result = self.app.get('/')
        assert json.loads(result.data)['items'][0]['closings_href'] == '/closings'

    def test_closing_index(self):
        datetime.datetime = Today
        result = self.app.get('/closings')
        closings = json.loads(result.data)['items']
        assert len(closings) == 5
        location_evans = closings[0]
        assert location_evans['location'] == 'Evans_(Galapago to Bannock)'
        assert location_evans['start_date'] == '2012-11-05'
        assert location_evans['end_date'] == '2013-07-30'
        assert location_evans['closing_type'] == ''
        assert location_evans['start_time'] == '00:00:00'
        assert location_evans['end_time'] == '23:59:59'
        assert location_evans['purpose'] == "Bridge Construction"

        all_locations = [closing['location'] for closing in closings]
        assert 'W Dartmouth Ave (S Golden Way - Colgate Dr)' not in all_locations

    def test_closing_by_date(self):
        result = self.app.get('/closings?on_date=2013-04-10')
        closings = json.loads(result.data)['items']
        assert len(closings) == 6

    def test_location(self):
        datetime.datetime = Today
        result = self.app.get('/closings')
        closings = json.loads(result.data)['items']
        assert closings[0]['geometry'] == { "type": "Point", "coordinates": [-104.9847179,39.737567]}

if __name__ == '__main__':
    unittest.main()
