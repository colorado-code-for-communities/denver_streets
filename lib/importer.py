import import_parent
import database
import requests
import datetime
from models import Closure

def read_closures():
    d = datetime.datetime.today().strftime('%Y-%m-%d')
    scraperwiki_query = "https://api.scraperwiki.com/api/1.0/datastore/sqlite?format=jsondict&name=denver_streets_and_sidewalks&query=select%20*%20from%20%60swdata%60%20where%20start_date%20%3C%20date('"+ d +"')%20and%20end_date%20%3E%20date('" + d + "')"
    r = requests.get(scraperwiki_query)
    return r.text

