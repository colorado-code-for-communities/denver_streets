import unittest
import os, sys
import datetime, json
os.environ["FLASK_ENV"] = "test"

parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0,parent_dir)
import denver_streets
from lib import importer

fixtures_dir = os.getcwd() + "/tests/fixtures"
sys.stdout = open(os.devnull, 'w')
