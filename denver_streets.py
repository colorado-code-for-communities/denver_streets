from flask import Flask, Response, url_for, request, json
from jinja2 import *
import os
import urllib2
import datetime
import database
import models
from models import *

def shutdown_session(exception=None):
    session.remove()

app = Flask(__name__)
env = Environment(loader=PackageLoader('denver_streets', 'templates'))

@app.route('/')
def index():
    items = ['closings']
    response = { 'items' : [] }
    [ response['items'].append({item+"_href": url_for(item)}) for item in items]
    response_data = json.dumps(response)
    response = Response(response_data, status=200, mimetype='application/json', headers={'Access-Control-Allow-Origin':'*'})
    return response

@app.route('/closings')
def closings():
    if request.args.get('on_date'):
        date_param = datetime.datetime.strptime(request.args.get('on_date'), "%Y-%m-%d")
    else:
        date_param = datetime.datetime.now()

    closings = database.session.query(Closing).filter(Closing.start_date <= date_param, Closing.end_date >= date_param).all()
    closings_array = []

    for closing in closings:
        closing_dict = closing.to_dict()
        closing_dict['geometry'] = json.loads(database.session.scalar(closing.geom.ST_AsGeoJSON()))
        closings_array.append(closing_dict)

    response = Response(json.dumps({'items': closings_array}), status=200, mimetype='application/json', headers={'Access-Control-Allow-Origin':'*'})
    return response

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
