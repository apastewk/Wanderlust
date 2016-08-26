from operator import attrgetter
from datetime import datetime, timedelta
import hashlib, uuid

################################################################################


def make_datetime_obj(date, time):
    """Combines start_date and start_time form inputs into a datetime object.

    >>> start_date = 2016-08-26
    ... start_time = 18:00

    >>> make_start_datetime_obj()
    ('2016-08-26' 18:00:00')

    """

    print date
    print time
    conv_date = datetime.strptime(date, "%Y-%m-%d").date()
    print conv_date
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


def hash_password(password):
    """Hashes a users password."""

     # salt = uuid.uuid4().hex
    return hashlib.sha224(password).hexdigest()[:20]




