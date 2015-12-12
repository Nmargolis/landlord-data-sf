"""Seed database from SF Open Data API"""

import requests
import json
from model import connect_to_db, db, Business, Location
from server import app
import pprint
import ast


# initialize pprint
pp = pprint.PrettyPrinter(indent=4)


def make_request():
    url = "https://data.sfgov.org/resource/nqzj-5ui2.json"
    response = requests.get(url)
    json_response = response.json()
    # pp.pprint(json_response[0])

    return json_response


def add_location(single_results_entry):
    """Takes a single business entry from API results, adds location to db, returns location_id"""

    # Initialize location_id to return
    location_id = ""

    lat = single_results_entry['location']['latitude']
    # print lat
    lon = single_results_entry['location']['latitude']
    # print lon

    human_address = single_results_entry['location']['human_address']
    # print human_address

    # Convert unicode object to dictionary
    human_addr = ast.literal_eval(human_address)
    # pp.pprint(human_addr)

    address = human_addr['address']
    # print address
    city = human_addr['city']
    # print city
    state = human_addr['state']
    # print state
    zipcode = human_addr['zip']
    # print zipcode

    # Query to see if location already in database.
    existing_loc = db.session.query(Location).filter_by(address=address, city=city, state=state, zipcode=zipcode).first()

    # If location is already in database, set location_id to that location's id
    if existing_loc:
        location_id = existing_loc.location_id
        print "Existing location_id: {}".format(location_id)

    # TO DO: Refactor to have separate function to query database and return location id if found

    # Otherwise, create new location, add it to the databse, and set location_id equal to the new location's id
    else:
        location = Location(lat=lat, lon=lon, address=address, city=city, state=state, zipcode=zipcode)

        db.session.add(location)
        db.session.commit()
        location_id = location.location_id
        print "New location_id: {}".format(location_id)

    return location_id


def load_locations_and_businesses(data_results_json):
    """Takes json api data and creates entries in Locations and Businesses tables"""

    # Add first 5 businesses locations to database
    for i in range(0, 5):
        add_location(data_results_json[i])


if __name__ == '__main__':

    api_data = make_request()
    connect_to_db(app)
    load_locations_and_businesses(api_data)
