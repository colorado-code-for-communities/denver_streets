from flask import Flask, Response, url_for, request, json
import os
import urllib2
import datetime

app = Flask(__name__)

@app.route('/hello')
def hello():
  return 'Hello world'

@app.route('/')
def index():
  response_data = json.dumps({ 'closures_href': url_for('closures') })
  response = Response(response_data, status=200, mimetype='application/json')
  return response

@app.route('/closures')
def closures():
  d = datetime.datetime.today()
  scraperwiki_query = "https://api.scraperwiki.com/api/1.0/datastore/sqlite?format=jsondict&name=denver_streets_and_sidewalks&query=select%20*%20from%20%60swdata%60%20where%20start_date%20%3E%20date('"+ d.strftime('%Y-%m-%d') +"')"

  scraperwiki_response = urllib2.urlopen(scraperwiki_query).read()
  response = Response(scraperwiki_response, status=200, mimetype='application/json')
  #return url_for('closure_id', closure_id=1)
  return response

@app.route('/closures/<int:closure_id>')
def closure_id():
  return ""
  # find closure with closure_id

if __name__ == '__main__':
  port = int(os.environ.get('PORT', 5000))
  app.run(host='0.0.0.0', port=port)
