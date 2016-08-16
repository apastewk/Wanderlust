"""Models for my database to store a users trip confirmation details."""

import os
from flask_sqlalchemy import SQLAlchemy
from flask import request

import datetime


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
    password = db.Column(db.String(64))

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
    departs_from = db.Column(db.String(20), nullable=True)
    airpt_code_dep = db.Column(db.String(3), nullable=True)
    ends_at = db.Column(db.DateTime, nullable=True)
    arrives_to = db.Column(db.String(20), nullable=True)
    airpt_code_arr = db.Column(db.String(3), nullable=True)
    duration = db.Column(db.Integer, nullable=True)
    rewards_num = db.Column(db.String(20), nullable=True)

    trip = db.relationship("Trip")
    passenger = db.relationship("Passenger")

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<Flight flight_id: {}, trip_id: {}, departs_from: {}, departs_at: {}, arrives_to: {}, arrives_at: {}".format(
            self.flight_id, self.trip_id, self.departs_from, self.departs_at,
            self.arrives_to, self.arrives_at)


class Passenger(db.Model):
    """Passengers on a particular flight."""

    __tablename__ = "passengers"

    passenger_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    flight_id = db.Column(db.Integer, db.ForeignKey("flights.flight_id"))
    passenger_name = db.Column(db.String(40), nullable=True)

    flight = db.relationship("Flight")

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<Passengers passenger_name: passenger_name, flight_id: flight_id>".format(
            self.passenger_name, self.flight_id)


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
    num_of_nights = db.Column(db.Integer, nullable=True)
    num_of_rooms = db.Column(db.Integer, nullable=True)
    rewards_num = db.Column(db.String(20), nullable=True)

    trip = db.relationship("Trip")

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<Hotel hotel_id: {}, trip_id: {}, hotel_name: {}, arrives_at: {}, departs_at: {}>".format(
            self.hotel_id, self.trip_id, self.hotel_name, self.arrives_at,
            self.departs_at)


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
    num_of_passengers = db.Column(db.Integer, nullable=True)

    trip = db.relationship("Trip")

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<Vendor vendor_id: {}, trip_id: {}, vendor_name: {}, departs_at: {}, arrives_at: {}>".format(
            self.vendor_id, self.trip_id, self.vendor_name, self.departs_at, self.arrives_at)


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


################################################################################

# Helepr Functions

def make_start_datetime_obj(start_date):
    """Combines start_date and start_time form inputs into a datetime object."""

    # s_time = 00:00
    s_date = request.form.get("start-date", None)
    s_time = request.form.get("start-time", None)
    s_date = str(s_date)
    s_time = str(s_time)


    conv_date = datetime.datetime.strptime(s_date, "%Y-%M-%d")
    conv_time = datetime.datetime.strptime(s_time, "%H:%M").time()

    return datetime.datetime.combine(conv_date, conv_time)
   


def make_end_datetime_obj(end_date):
    """Combines end_date and end_time form inputs into a datetime object."""

    e_date = request.form.get("end-date", None)
    e_time = request.form.get("end-time", None)
    e_date = str(e_date)
    e_time = str(e_time)

    conv_date = datetime.datetime.strptime(e_date, "%Y-%M-%d")
    conv_time = datetime.datetime.strptime(e_time, "%H:%M").time()

    return datetime.datetime.combine(conv_date, conv_time)


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
