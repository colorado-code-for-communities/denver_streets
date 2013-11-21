Denver Street Construction API
==============

API for Denver Streets/Sidewalks closings.

Currently the way to look up street closings in Denver is to [browse through a PDF](www.denvergov.org/streetclosures)
that's released biweekly. To search, the website instructs you to do the following:

```
If looking for a particular street, hit Ctrl + F to find it within the document
```

The API is to turns this:

![](https://dl.dropboxusercontent.com/u/2372981/denverclosings.png)

into this: 

```javascript
{
  "end_date": "2014-07-01", 
  "start_date": "2013-08-31", 
  "geometry":
     {
      "type": "LineString", 
      "coordinates": [[-104.9425648, 39.7114694], [-104.941355, 39.7114643]]
     }, 
     "start_time": "00:00:00", 
     "end_time": "23:59:59", 
     "purpose": "ROW Occupancy",
     "closing_type": "Close Sidewalk", 
     "id": 455, 
     "location": "Alameda ave: Jackson st - Harrison st"
}
```

and allow users to query for closings based on location, date, time, etc.

Using
==============

GET: `/closings`

Returns a list of current closings.

GET: `/closings?on_date=YYYY-MM-DD`

Returns a list of street closings on specific date

TODO:

GET: `/closings?location=`

Return a list of street closings near a location.


Development
==============
You need:
* Python 2.7.3
* Postgresql 9.1
* Postgis for Postgresql 9.1 (http://linfiniti.com/2012/05/installing-postgis-2-0-on-ubuntu/). 
  * For OSX users, you can install via brew
  * For Linux users, you can install via your package management of choice
 

=======

To start the server locally, run `python denver_streets.py` and visit 
http://0.0.0.0:5000 in your browser

=======
Database setup
(From http://www.geoalchemy.org/tutorial.html)
<!-- sudo su postgres -->

```sh
# Create a new superuser if gisuser does not exist already
createuser -P -s denverstreetsuser
```

Copy config.yaml.example to config.yaml. Open it up.
Edit the database settings with the correct username and password you set.

Fill in postgis_extensions_dir with the postgis install directory that contains your postgis.sql files.

From the app root directory and run the following:
```
./bin/setup_db
```

This will create the databases (development and test) with the proper python extensions. 

To drop tables (not the database!), run ```./bin/drop_db```

If you want to make sure that PostGIS is correctly installed, run the following:
sudo -u postgres psql -d denver_streets[_test] -c "SELECT postgis_full_version()"
You should get something like:

                                     postgis_full_version
------------------------------------------------------------------------------------------------------
POSTGIS="1.5.2" GEOS="3.2.2-CAPI-1.6.2" PROJ="Rel. 4.7.1, 23 September 2009" LIBXML="2.7.7" USE_STATS
(1 row)


Tests are currently a giant mess. Sorry! To run tests, run `./run_tests`. 
