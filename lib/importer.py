import import_parent
import denver_streets
from street_parser import StreetParser
from geoalchemy2 import *
import requests
import datetime
import json
from sqlalchemy.sql.expression import func
from sqlalchemy.sql import exists

Closing = denver_streets.models.Closing
session = denver_streets.database.session
street_parser = StreetParser()

def read_closings():
    d = datetime.datetime.today().strftime('%Y-%m-%d')
    scraperwiki_query = "https://api.scraperwiki.com/api/1.0/datastore/sqlite?format=jsondict&name=denver_streets_and_sidewalks&query=select%20*%20from%20%60swdata%60"
    r = requests.get(scraperwiki_query)
    return r.text

def import_closings(closing_json):
    closing_json = json.loads(closing_json)
    for closing in closing_json:
        import_closing(closing)

def import_closing(closing):
    row_exists = session.query(exists().where(Closing.location == closing['location'].rstrip())).scalar()

    if row_exists:
        print 'row exists'
    if not row_exists:
        closing_row = Closing(
                end_date=closing['end_date'],
                start_date=closing['start_date'],
                location=closing['location'].rstrip(),
                closing_type=closing['type'].rstrip(),
                purpose=closing['purpose'].rstrip(),
                start_time=start_time(closing['time']),
                end_time=end_time(closing['time']),
                geom=street_parser.geolocater(closing['location'])
                )
        print "adding " + closing['location']
        session.add(closing_row)
        session.commit()

def start_time(time_str):
    if '24 hrs' in time_str:
        return datetime.time(0, 0, 0)

def end_time(time_str):
    if '24 hrs' in time_str:
        return datetime.time(23, 59, 59)

def main():
    import_closings(read_closings())

if __name__ == '__main__':
    main()
