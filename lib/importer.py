import import_parent
import denver_streets
from street_parser import StreetParser
from geoalchemy import *
import requests
import datetime
import json
from sqlalchemy.sql.expression import func

Closure = denver_streets.models.Closure
session = denver_streets.database.session
street_parser = StreetParser()

def read_closures():
    d = datetime.datetime.today().strftime('%Y-%m-%d')
    scraperwiki_query = "https://api.scraperwiki.com/api/1.0/datastore/sqlite?format=jsondict&name=denver_streets_and_sidewalks&query=select%20*%20from%20%60swdata%60%20where%20start_date%20%3C%20date('"+ d +"')%20and%20end_date%20%3E%20date('" + d + "')"
    r = requests.get(scraperwiki_query)
    return r.text

def import_closures(closure_json):
    closure_json = json.loads(closure_json)
    for closure in closure_json:
        import_closure(closure)

def import_closure(closure):
    cl = Closure(
            end_date=closure['end_date'],
            start_date=closure['start_date'],
            location=closure['location'].rstrip(),
            closure_type=closure['type'].rstrip(),
            purpose=closure['purpose'].rstrip(),
            start_time=start_time(closure['time']),
            end_time=end_time(closure['time']),
            geom=func.ST_GeomFromText(street_parser.geolocater(closure['location']), 4326)
            )
    print "adding " + closure['location']
    session.add(cl)
    session.commit()

def start_time(time_str):
    if '24 hrs' in time_str:
        return datetime.time(0, 0, 0)

def end_time(time_str):
    if '24 hrs' in time_str:
        return datetime.time(23, 59, 59)
