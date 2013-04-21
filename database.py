from sqlalchemy import *
from sqlalchemy.orm import *
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine('postgresql://gisuser:abc123@localhost/denver_streets', echo=True)
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
