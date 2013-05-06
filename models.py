import denver_streets
from sqlalchemy import *
from geoalchemy import *
from geoalchemy.postgis import PGComparator
import datetime
import os

Base = denver_streets.database.Base

class Closure(Base):
    __tablename__ = 'closures'
    id = Column(Integer, primary_key=True)
    name = Column(String(255), unique=True)
    location = Column(String(256), unique=True)
    closure_type = Column(String(255))
    purpose = Column(String(255))
    start_date = Column(Date())
    end_date = Column(Date())
    start_time = Column(Time())
    end_time = Column(Time())
    geom = GeometryColumn(LineString(2))

    def __init__(self, location=None, closure_type=None, purpose="", start_date=datetime.datetime.now(), end_date=None, start_time=None, end_time=None, geom=""):
        self.location = location
        self.closure_type = closure_type
        self.purpose = purpose
        self.start_date = start_date
        self.end_date = end_date
        self.start_time = start_time
        self.end_time = end_time

    def __repr__(self):
        return '<Location %r>' % self.location

    def to_dict(self):
        sql_dict = {}
        for column_name in self.__table__.c.keys():
            sql_dict[column_name] = getattr(self, column_name)
            if type(sql_dict[column_name]) == datetime.date or type(sql_dict[column_name]) == datetime.time:
                sql_dict[column_name] = str(sql_dict[column_name])

        return sql_dict

GeometryDDL(Closure.__table__)
