import denver_streets
from sqlalchemy import *
from geoalchemy2 import *
import datetime
import os

Base = denver_streets.database.Base

class Closing(Base):
    __tablename__ = 'closings'
    id = Column(Integer, primary_key=True)
    location = Column(String(256), unique=True)
    closing_type = Column(String(255))
    purpose = Column(String(255))
    start_date = Column(Date())
    end_date = Column(Date())
    start_time = Column(Time())
    end_time = Column(Time())
    geom = Column(Geometry(srid=4326))

    def __init__(self, location=None, closing_type=None, purpose="", start_date=datetime.datetime.now(), end_date=None, start_time=None, end_time=None, geom=""):
        self.location = location
        self.closing_type = closing_type
        self.purpose = purpose
        self.start_date = start_date
        self.end_date = end_date
        self.start_time = start_time
        self.end_time = end_time
        self.geom = WKTElement(geom, srid=4326)

    def __repr__(self):
        return '<Location %r>' % self.location

    def to_dict(self):
        sql_dict = {}
        for column_name in self.__table__.c.keys():
            if column_name == 'geom':
                continue
            sql_dict[column_name] = getattr(self, column_name)
            if type(sql_dict[column_name]) == datetime.date or type(sql_dict[column_name]) == datetime.time:
                sql_dict[column_name] = str(sql_dict[column_name])

        return sql_dict

