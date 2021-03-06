"""Model and functions"""
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Location(db.Model):
    """Class for locations table"""

    __tablename__ = "Locations"

    location_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    lat = db.Column(db.Text)
    lon = db.Column(db.Text)
    address = db.Column(db.Text)
    city = db.Column(db.Text)
    state = db.Column(db.Text)
    zipcode = db.Column(db.Text)

    businesses = db.relationship('Business',
                                 secondary='BusinessLocations',
                                 backref='location')

    def __repr__(self):
        return "<Location location_id = {} lat = {} lon = {} address = {} city = {} state = {} zipcode = {}>".format(
            self.location_id, self.lat, self.lon, self.address, self.city, self.state, self.zipcode)


class Business(db.Model):
    """Class for businesses table"""

    __tablename__ = "Businesses"

    business_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    dba_name = db.Column(db.Integer)
    ownership_name = db.Column(db.Text)
    class_code = db.Column(db.Text)
    pbc_code = db.Column(db.Text)

    def __repr__(self):
        return "<Business business_id = {} dba_name = {} ownership_name = {} class_code = {} pbc_code = {}>".format(
            self.business_id, self.dba_name, self.ownership_name, self.class_code, self.pbc_code)


# TO DO: Create separate table for ownership name and/or dba_name, since one owner or business could have multiple pbc codes (maybe)


class BusinessLocation(db.Model):
    "Association table between Business and Location"

    __tablename__ = "BusinessLocations"

    businesslocation_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    business_id = db.Column(db.Integer, db.ForeignKey('Businesses.business_id'))
    location_id = db.Column(db.Integer, db.ForeignKey('Locations.location_id'))

    business = db.relationship('Business', backref='businesslocation')
    location = db.relationship('Location', backref='businesslocation')

    def __repr__(self):
        return "<BusinessLocation business_location_id = {} business_id = {}, location_id = {}>".format(
            self.businesslocation_id, self.business_id, self.location_id)

##############################################################################
# Helper functions


def connect_to_db(app):
    """Connect the database to our Flask app."""
    # Configure to use our SQLite database
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///sfapartments.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
    db.app = app
    db.init_app(app)

if __name__ == "__main__":

    from server import app

    connect_to_db(app)
    print "Connected to DB."

    db.create_all()
    print "Created tables."
