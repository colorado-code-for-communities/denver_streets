from test_helpers import *
from lib.street_parser import StreetParser

class LocationParserTests(unittest.TestCase):
    def setUp(self):
        self.location_strings = [
                '10th AVE: SHERIDAN TO YATES',
                'Evans_(Galapago to Bannock)',
                '12th Ave - Colorado to Hale Parkway/Albion',
                '12th St: Welton - Glenarm',
                '17th St, NB: Wewatta to Chestnut',
                '17th St: Chestnut to Wewatta',
                '17th St: SB: Chestnut to Wewatta',
                '46th ave: w.bound lanes.(chambers - granby) TCP#19.1',
                '56th Ave (Quebec to Havana) E. & W. Bound MHT 43 & 45'
                ]

    def testParseLocationStringLine(self):
        assert StreetParser().find_location(self.location_strings[0]) == ['10th ave', 'sheridan', 'yates']
        assert StreetParser().geolocater(self.location_strings[0]) == 'LINESTRING(-105.0532578 39.7331141, -105.0510184 39.7330965)'

    def testParseLocationStringPoint(self):
        assert StreetParser().find_location(self.location_strings[1]) == 'Evans_(Galapago to Bannock)'
        assert 'POINT(' in StreetParser().geolocater(self.location_strings[1])

if __name__ == '__main__':
    unittest.main()
