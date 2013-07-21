from test_helpers import *

database = denver_streets.database
Closing = denver_streets.Closing

class ImporterTests(unittest.TestCase):
    def setUp(self):
        # set up test db
        self.closing_json = open(fixtures_dir + '/importer_test_fixtures.txt').read()
        database.init_db()

    def tearDown(self):
        database.drop_db()

    def testImportClosings(self):
        importer.import_closings(self.closing_json)
        self.assertEquals(len(database.session.query(Closing).all()), 6)

    # Start time and end time should be 00:00:00 to 11:59:59
    def testImportClosingTime(self):
        importer.import_closings(self.closing_json)
        closing = database.session.query(Closing).all()[0]
        self.assertEquals(closing.start_time, datetime.time(0, 0, 0))
        self.assertEquals(closing.end_time, datetime.time(23, 59, 59))

    def testImportClosingLocation(self):
        importer.import_closings(self.closing_json)
        closings = database.session.query(Closing).all()
        assert closings[0].location == 'Evans_(Galapago to Bannock)'
        assert closings[1].location == 'Pecos St'
        assert closings[2].location == 'W Dartmouth Ave (S Golden Way - Colgate Dr)'

    def testImportClosingType(self):
        importer.import_closings(self.closing_json)
        closings = database.session.query(
                Closing).filter(
                Closing.location.like('W Dartmouth%')).first()
        self.assertEquals(closings.closing_type, 'Close 1st Traffic Lane')


if __name__ == '__main__':
    unittest.main()
