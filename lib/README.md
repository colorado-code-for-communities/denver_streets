(From http://www.geoalchemy.org/tutorial.html)
```sh
sudo su postgres
createdb -E UNICODE denver_streets
createlang plpgsql denver_streets

psql -d denver_streets -f /usr/share/postgresql/9.1/contrib/postgis-1.5/postgres.sql
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
