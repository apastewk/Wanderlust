"""Models for my database to store a users trip confirmation details."""

import os
from flask_sqlalchemy import SQLAlchemy

from operator import attrgetter
from datetime import datetime, timedelta


# This is the connection to the PostreSQL database.  Getting the through the
# Flask-SQLAlchemy helper library.

db = SQLAlchemy()


################################################################################

# Model definitions

class User(db.Model):
    """User of something website."""

    __tablename__ = "users"

    user_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    firstname = db.Column(db.String(20))
    lastname = db.Column(db.String(20))
    email = db.Column(db.String(64))
    password = db.Column(db.String(200))

    trip = db.relationship("Trip")

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<User user_id: {} email: {}>".format(self.user_id, self.email)


class Trip(db.Model):
    """A users trip details."""

    __tablename__ = "trips"

    trip_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"))
    destination = db.Column(db.String(64))
    trip_name = db.Column(db.String(64))
    start_date = db.Column(db.DateTime)
    end_date = db.Column(db.DateTime)
    notes = db.Column(db.String(500), nullable=True)

    user = db.relationship("User")
    flight = db.relationship("Flight")
    hotel = db.relationship("Hotel")
    car_rental = db.relationship("CarRental")
    public_transportation = db.relationship("PublicTransportation")
    event = db.relationship("Event")
    meeting = db.relationship("Meeting")


    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<Trip user_id: {} trip_id: {} destination: {}>".format(self.user_id,
            self.trip_id, self.destination)


class Flight(db.Model):
    """A users flight details."""

    __tablename__ = "flights"

    flight_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    trip_id = db.Column(db.Integer, db.ForeignKey("trips.trip_id"))
    confirmation_num = db.Column(db.String(20), nullable=True)
    airline = db.Column(db.String(20), nullable=True)
    flight_num = db.Column(db.String(10), nullable=True)
    starts_at = db.Column(db.DateTime, nullable=True)
    departs_from = db.Column(db.String(64), nullable=True)
    airpt_code_dep = db.Column(db.String(3), nullable=True)
    ends_at = db.Column(db.DateTime, nullable=True)
    arrives_to = db.Column(db.String(64), nullable=True)
    airpt_code_arr = db.Column(db.String(3), nullable=True)
    duration = db.Column(db.Integer, nullable=True)
    rewards_num = db.Column(db.String(20), nullable=True)

    trip = db.relationship("Trip")

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<Flight flight_id: {}, trip_id: {}, departs_from: {}, starts_at: {}, arrives_to: {}, ends_at: {}".format(
            self.flight_id, self.trip_id, self.departs_from, self.starts_at,
            self.arrives_to, self.ends_at)


class Hotel(db.Model):
    """A users hotel details."""

    __tablename__ = "hotels"

    hotel_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    trip_id = db.Column(db.Integer, db.ForeignKey("trips.trip_id"))
    confirmation_num = db.Column(db.String(20), nullable=True)
    hotel_name = db.Column(db.String(40), nullable=True)
    address = db.Column(db.String(100), nullable=True)
    starts_at = db.Column(db.DateTime, nullable=True)
    ends_at = db.Column(db.DateTime, nullable=True)
    room_type = db.Column(db.String(20), nullable=True)

    trip = db.relationship("Trip")

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<Hotel hotel_id: {}, trip_id: {}, hotel_name: {}, ends_at: {}, starts_at: {}>".format(
            self.hotel_id, self.trip_id, self.hotel_name, self.ends_at,
            self.starts_at)


class CarRental(db.Model):
    """A users car rental details."""

    __tablename__ = "car_rentals"

    rental_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    trip_id = db.Column(db.Integer, db.ForeignKey("trips.trip_id"))
    confirmation_num = db.Column(db.String(20), nullable=True)
    agency_name = db.Column(db.String(20), nullable=True)
    starts_at = db.Column(db.DateTime, nullable=True)
    pickup_from = db.Column(db.String(100), nullable=True)
    ends_at = db.Column(db.DateTime, nullable=True)
    dropoff_to = db.Column(db.String(100), nullable=True)
    drivers_name = db.Column(db.String(40), nullable=True)
    car_type = db.Column(db.String(20), nullable=True)
    rewards_num = db.Column(db.String(20), nullable=True)

    trip = db.relationship("Trip")

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<Car rental rental_id: {}, agency_name: {}, starts_at: {}, ends_at: {}>".format(
            self.rental_id, self.agency_name, self.starts_at, self.ends_at)


class PublicTransportation(db.Model):
    """A users public transportation details."""

    __tablename__ = "public_transportations"

    vendor_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    trip_id = db.Column(db.Integer, db.ForeignKey("trips.trip_id"))
    confirmation_num = db.Column(db.String(20), nullable=True)
    vendor_name = db.Column(db.String(20), nullable=True)
    departs_from = db.Column(db.String(64), nullable=True)
    starts_at = db.Column(db.DateTime, nullable=True)
    arrives_to = db.Column(db.String(64), nullable=True)
    ends_at = db.Column(db.DateTime, nullable=True)
    travelers_name = db.Column(db.String(40), nullable=True)
    duration = db.Column(db.Integer, nullable=True)
    transport_num = db.Column(db.String(20), nullable=True)

    trip = db.relationship("Trip")

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<Vendor vendor_id: {}, trip_id: {}, vendor_name: {}, starts_at: {}, ends_at: {}>".format(
            self.vendor_id, self.trip_id, self.vendor_name, self.starts_at, self.ends_at)


class Event(db.Model):
    """A users event details."""

    __tablename__ = "events"

    event_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    trip_id = db.Column(db.Integer, db.ForeignKey("trips.trip_id"))
    confirmation_num = db.Column(db.String(20), nullable=True)
    event_name = db.Column(db.String(40), nullable=True)
    starts_at = db.Column(db.DateTime, nullable=True)
    address = db.Column(db.String(100), nullable=True)

    trip = db.relationship("Trip")

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<Event event_id: {}, trip_id: {}, confirmation_num: {}, event_name: {}, starts_at: {}, address: {}>".format(
            self.event_id, self.trip_id, self.confirmation_num, self.event_name, self.starts_at, self.address)


class Meeting(db.Model):
    """A users meeting details."""

    __tablename__ = "meetings"

    meeting_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    trip_id = db.Column(db.Integer, db.ForeignKey("trips.trip_id"))
    meeting_subject = db.Column(db.String(250), nullable=True)
    starts_at = db.Column(db.DateTime, nullable=True)
    address = db.Column(db.String(100), nullable=True)

    trip = db.relationship("Trip")

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<Meeting meeting_id: {}, trip_id: {} meeting_subject: {}, starts_at: {}>".format(
            self.meeting_id, self.trip_id, self.meeting_subject, self.starts_at)

def example_data():
    """Create some sample data."""

    meeting = Meeting(trip_id=1,
                      meeting_subject="Uber",
                      starts_at=datetime.strptime("2016-08-26 18:00:00", "%Y-%m-%d %H:%M"),
                      address="123 Cooper St, Oakland, CA")

    trip = Trip(user_id=1,
                start_date=datetime.strptime("2016-08-10 00:00:00", "%Y-%m-%d %H:%M"),
                end_date=datetime.strptime("2016-09-20 00:00:00", "%Y-%m-%d %H:%M"),
                trip_name="Rome",
                destination="Rome")

    user = User(firstname="Lauren",
                lastname="Budd",
                email="laurenb@gmail.com",
                password="test123")

    db.session.add_all([meeting, trip, user])
    db.session.commit()

################################################################################

# Helepr Functions


def connect_to_db(app):
    """Connect the database to Flask app."""

    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("DATABASE_URL", "postgresql:///trips")
    # app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
    db.app = app
    db.init_app(app)


if __name__ == "__main__":
    """Will conenct to the db."""

    from server import app
    connect_to_db(app)
    db.create_all()
    print "Connected to DB."
