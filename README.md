denver_streets
==============

API for Denver Streets/Sidewalks closures

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
```sh
sudo su postgres
createdb -E UNICODE denver_streets
createlang plpgsql denver_streets

psql -d denver_streets -f /usr/share/postgresql/9.1/contrib/postgis-1.5/postgis.sql
psql -d denver_streets -f /usr/share/postgresql/9.1/contrib/postgis-1.5/spatial_ref_sys.sql

# Create a new user if gisuser does not exist already
createuser -P gisuser

# Grant permissions to user gisuser
psql denver_streets
grant all on database denver_streets to "gisuser";
grant all on spatial_ref_sys to "gisuser";
grant all on geometry_columns to "gisuser";
\q
```
