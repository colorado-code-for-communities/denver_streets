Denver Street Construction API
==============

API for Denver Streets/Sidewalks closures

Using
==============

GET: `/`

GET: `/closures`

Returns a list of current closures.

GET: `/closures?current_location=??&radius=1`

Returns all closures within a radius in miles (default radius will be equal to 1).

Development
==============
Pivotal Tracker:
https://www.pivotaltracker.com/projects/768887

You need:
* Python 2.7.3
* Postgresql 9.1
* Postgis for Postgresql 9.1 (http://linfiniti.com/2012/05/installing-postgis-2-0-on-ubuntu/). 
  * For OSX users, you can install via brew
 

=======

To start the server locally, run `python app.py` and visit 
http://0.0.0.0:5000 in your browser

=======
Database setup
(From http://www.geoalchemy.org/tutorial.html)
<!-- sudo su postgres -->

```sh
createdb -E UNICODE denver_streets
createlang plpgsql denver_streets

psql -d denver_streets -f (your postgis install directory)/postgis.sql
psql -d denver_streets -f (your postgis install directory)/spatial_ref_sys.sql

# Create a new user if gisuser does not exist already
createuser -P gisuser

# Grant permissions to user gisuser
psql denver_streets
grant all on database denver_streets to "gisuser";
grant all on spatial_ref_sys to "gisuser";
grant all on geometry_columns to "gisuser";
\q
```

Open up your python REPL in the app root directory and type the following:
```python
import database
database.init_db()
```

This will create the tables.

To drop tables (not the database!), type ```database.drop_db()``` in said REPL session.


Tests are currently a giant mess. Sorry! To run tests, run `./run_tests`. 
