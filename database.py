from sqlalchemy import *
from sqlalchemy.orm import *
from sqlalchemy.ext.declarative import declarative_base
from geoalchemy import *
import os

try:
    if os.environ['FLASK_ENV'] == 'test':
        database_name = "denver_streets_test"
        database_user = 'gisuser_test'
        database_pass = ''
    else:
        database_name = "denver_streets"
        database_user = 'gisuser'
        database_pass = 'abc123'
except:
    database_name = 'denver_streets'
    database_user = 'gisuser'
    database_pass = 'abc123'
    # regular db

engine = create_engine('postgresql://'+database_user+':'+database_pass+'@localhost/' + database_name)
session = scoped_session(sessionmaker(bind=engine))
metadata = MetaData(engine)
Base = declarative_base(metadata=metadata)
Base.query = session.query_property()

def init_db():
    import models
    metadata.create_all(bind=engine)
    session.commit()

def drop_db():
    import models
    session.close()
    metadata.drop_all(bind=engine)

def setup_db():
    engine = create_engine('postgresql://postgres@localhost/postgres')
    conn = engine.connect()
    conn.execute('commit')
    conn.execute('create database ' + database_name)
    conn.close()

def destroy_db():
    engine = create_engine('postgresql://postgres@localhost/postgres')
    conn = engine.connect()
    conn.execute('commit')
    conn.execute('drop database ' + database_name)
    conn.close()

