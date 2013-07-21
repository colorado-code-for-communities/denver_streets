Denver Street Construction API
==============

API for Denver Streets/Sidewalks closings

Using
==============

GET: `/`

GET: `/closures`

Returns a list of current closings.

GET: `/closures?on_date=YYYY-MM-DD`

Returns a list of street closings on specific date

GET: `/closures?current_location=??&radius=1`

Returns all closings within a radius in miles (default radius will be equal to 1).

Development
==============
Pivotal Tracker:
https://www.pivotaltracker.com/projects/768887

You need:
* Python 2.7.3
* Postgresql 9.1
* Postgis for Postgresql 9.1 (http://linfiniti.com/2012/05/installing-postgis-2-0-on-ubuntu/). 
  * For OSX users, you can install via brew
  * For Linux users, you can install via your package management of choice
 

=======

To start the server locally, run `python app.py` and visit 
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
