import import_parent
import app
import requests
import datetime
import json

Closure = app.models.Closure
session = app.database.session

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
            location=closure['location'],
            closure_type=closure['type'],
            purpose=closure['purpose']
            )
    print "adding " + closure['location']
    session.add(cl)
    session.commit()
