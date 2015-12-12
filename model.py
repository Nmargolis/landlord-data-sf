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


class Business(db.Model):
    """Class for businesses table"""

    __tablename__ = "Businesses"

    business_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    dba_name = db.Column(db.Integer)
    ownership_name = db.Column(db.Text)
    class_code = db.Column(db.Text)
    pbc_code = db.Column(db.Text)
    location_id = db.Column(db.Integer, db.ForeignKey('Locations.location_id'))

    location = db.relationship('Location', backref='businesses')




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
