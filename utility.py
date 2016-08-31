from operator import attrgetter
from datetime import datetime, timedelta
import hashlib, uuid
from model import Trip

################################################################################


def hash_password(password):
    """Hashes a users password."""

     # salt = uuid.uuid4().hex
    return hashlib.sha224(password).hexdigest()[:20]


def make_datetime_obj(date, time):
    """Combines start_date and start_time form inputs into a datetime object.

    >>> date = 2016-08-26
    ... time = 18:00

    >>> make_start_datetime_obj()
    ('2016-08-26' 18:00:00')

    """

    conv_date = datetime.strptime(date, "%Y-%m-%d").date()
    conv_time = datetime.strptime(time, "%H:%M").time()

    return datetime.combine(conv_date, conv_time)


def get_trip_entities(trip):
    """Creates a list of sql objects and sorts them by date"""

    results = trip.flight + trip.hotel + trip.car_rental + trip.public_transportation + trip.event + trip.meeting
    sorted_results = sorted(results, key=attrgetter('starts_at'))
    return sorted_results


# def daterange(start_date, end_date):
#     """Determines"""
#     for n in range(int((end_date - start_date).days)):
#         yield start_date + timedelta(n)


def create_trip_entities_dict(trip_entities):
    """Converts a list of trip entities into a modified dictionary."""

    trip_entities = [entity.__dict__ for entity in trip_entities]

    for entity in trip_entities:
        if "_sa_instance_state" in entity:
            del entity["_sa_instance_state"]
        if "starts_at" in entity:
            entity["start_time"] = entity["starts_at"].strftime("%H:%M")
            entity["starts_at"] = entity["starts_at"].strftime("%a, %b %d, %Y")
        if "ends_at" in entity:
            entity["end_time"] = entity["ends_at"].strftime("%H:%M")
            entity["ends_at"] = entity["ends_at"].strftime("%a, %b %d, %Y")
        else:
            continue

    return trip_entities


def modifies_user_trips(trips):
    """Accesses all of the trips associated with a user."""

    trips_list = []

    for trip in trips:
        if trip:
            start_date = trip.start_date.strftime("%a, %b %d, %Y")
            end_date = trip.end_date.strftime("%a, %b %d, %Y")
            trip_detail = (trip.trip_name, start_date, end_date, trip.notes, trip.trip_id)
            trips_list.append(trip_detail)
        else:
            return None

    return trips_list


def count_user_trips(session_user_id):
    """Counts how many trips are in the past and how many are upcoming."""

    all_trips = Trip.query.filter(Trip.user_id == session_user_id).order_by(Trip.start_date).all()

    future_trips = 0
    past_trips = 0
    future_trips_list = []
    past_trips_list = []
    todays_date = datetime.now()

    for trip in all_trips:
        if trip.start_date <= todays_date:
            past_trips += 1
            past_trips_list.append(trip)

        else:
            future_trips += 1
            future_trips_list.append(trip)

    return [(future_trips, past_trips), (future_trips_list, past_trips_list)]

