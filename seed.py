"""Seed database from SF Open Data API"""

import requests
import json
from model import connect_to_db, db, Business, Location, BusinessLocation
from server import app
import pprint
import ast


# initialize pretty print to print out json and dictionaries in readable format
pp = pprint.PrettyPrinter(indent=4)


def make_request():
    """Makes request to SF Open Data API and return the response in json form"""

    url = "https://data.sfgov.org/resource/nqzj-5ui2.json"
    response = requests.get(url)
    json_response = response.json()
    # pp.pprint(json_response[0])

    return json_response


def add_location(single_results_entry):
    """Takes a single business entry from API results, adds location to db if it isn't already there, returns location_id"""

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


def add_business(single_results_entry):
    """Takes a single business entry from API results, adds business to db if not already there, returns business_id"""

    # Initialize business_id to return
    business_id = ""

    dba_name = single_results_entry['dba_name']
    ownership_name = single_results_entry['ownership_name']
    class_code = single_results_entry['class_code']
    pbc_code = single_results_entry['pbc_code']

    # Query to see if business already in database.
    existing_business = db.session.query(Business).filter_by(dba_name=dba_name, ownership_name=ownership_name, class_code=class_code, pbc_code=pbc_code).first()

    # If business is already in database, set business_id to that business' id
    if existing_business:
        business_id = existing_business.business_id
        print "Existing business_id: {}".format(business_id)

    # TO DO: Refactor to have separate function to query database and return business_id if found

    # Otherwise, create new business, add it to the databse, and set business_id to the new business' id
    else:
        business = Business(dba_name=dba_name, ownership_name=ownership_name, class_code=class_code, pbc_code=pbc_code)
        db.session.add(business)
        db.session.commit()
        business_id = business.business_id
        print "New business_id: {}".format(business_id)

    return business_id


def add_businesslocation(business_id, location_id):
    """Add BusinessLocation association to database if not already there"""

    # Query to see if businesslocation association already in database
    existing_busloc = db.session.query(BusinessLocation).filter_by(business_id=business_id, location_id=location_id).first()

    if existing_busloc:
        print "Existing businesslocation_id: {}".format(existing_busloc.businesslocation_id)

    # Otherwise, add businesslocation association to database
    else:
        new_busloc = BusinessLocation(business_id=business_id, location_id=location_id)
        db.session.add(new_busloc)
        db.session.commit()
        print "New businesslocation_id: {}".format(new_busloc.businesslocation_id)


def load_locations_and_businesses(data_results_json):
    """Takes json api data and creates entries in Locations and Businesses tables"""

    # Add businsess
    for business in data_results_json:
        location_id = add_location(business)
        business_id = add_business(business)
        add_businesslocation(business_id, location_id)


if __name__ == '__main__':

    api_data = make_request()
    connect_to_db(app)
    load_locations_and_businesses(api_data)
