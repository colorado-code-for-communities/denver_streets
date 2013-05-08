import os, re, database
import requests
from models import Closure
import time

class StreetParser():
    def geolocate(self, streets):
        if len(streets) == 3 and streets.__class__ == [].__class__:
            street1, street2, street3 = streets
            point1 = self.geocode_intersection(street1, street2)
            point2 = self.geocode_intersection(street1, street3)
            return 'LINESTRING('+point1+", "+point2+")"
        else:
            return 'LINESTRING('+self.geocode_point(streets)+', '+ self.geocode_point(streets) +')'

    def geocode_point(self, streets):
        address = streets + " Denver, CO"
        geocode_url = 'http://maps.googleapis.com/maps/api/geocode/json?address='+address+'&sensor=false&output=json'
        location_result = requests.get(geocode_url).json()
        if location_result['status'] == 'OVER_QUERY_LIMIT':
            time.sleep(2)
            location_result = requests.get(geocode_url).json()
        location = location_result['results'][0]['geometry']['location']
        return "" + str(location['lng']) + " " + str(location['lat'])

    def geocode_intersection(self, street1, street2):
        intersection = street1 + ' and ' + street2 + ", Denver, CO"
        geocode_url = 'http://maps.googleapis.com/maps/api/geocode/json?address='+intersection+'&sensor=false&output=json'
        location_result = requests.get(geocode_url).json()
        if location_result['status'] == 'OVER_QUERY_LIMIT':
            time.sleep(2)
            location_result = requests.get(geocode_url).json()

        location = location_result['results'][0]['geometry']['location']
        return "" + str(location['lng']) + " " + str(location['lat'])

    def find_locations(self):
        closures = database.session().query(Closure).all()

        for closure in closures:
            locations = self.find_location(closure.location)
            self.geolocate(locations)

    def find_location(self, location_string):
        street_segment_regex = re.compile('(.+):(.+)(to|-)(.+)')
        match = street_segment_regex.match(location_string.lower())
        if match:
            street1, street2 = match.group(1, 2)
            street3 = match.group(4)

            return [street1.strip(), street2.strip(), street3.strip()]
        return location_string

    def geolocater(self, location_string):
        return self.geolocate(self.find_location(location_string))

