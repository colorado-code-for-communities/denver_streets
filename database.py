from sqlalchemy import *
from sqlalchemy.orm import *
from sqlalchemy.ext.declarative import declarative_base

try:
    if os.environ['FLASK_ENV'] == 'test':
        database_name = "denver_streets_test"
    else:
        database_name = "denver_streets"
except:
    database_name = 'denver_streets'
    # regular db

engine = create_engine('postgresql://gisuser:abc123@localhost/' + database_name)

session = scoped_session(sessionmaker(bind=engine))

Base = declarative_base()
Base.query = session.query_property()

def init_db():
    import models
    Base.metadata.create_all(bind=engine)
    session.commit()

def drop_db():
    import models
    session.close()
    Base.metadata.drop_all(bind=engine)

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
    conn.execute('drop database' + database_name)
    conn.close()

