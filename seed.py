"""Seed database from SF Open Data API"""

import requests
import json
from model import connect_to_db, db, Business, Location
from server import app


def load_locations_and_businesses(data_results):
    """Takes json api data and creates entries in Locations and Businesses tables"""
    pass
