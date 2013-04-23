import app
from sqlalchemy import Column, Integer, String, Date, Time
from datetime import datetime
import os

Base = app.database.Base

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

    def __init__(self, name=None, location=None, closure_type=None, purpose="", start_date=datetime.now(), end_date=None, start_time=None, end_time=None):
        self.name = name
        self.location = location
        self.closure_type = closure_type
        self.purpose = purpose
        self.start_date = start_date
        self.end_date = end_date
        self.start_time = start_time
        self.end_time = end_time

    def __repr__(self):
        return '<Name %r>' % self.name
