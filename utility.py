from flask import request
from operator import attrgetter
from datetime import datetime, timedelta

################################################################################

def make_start_datetime_obj():
    """Combines start_date and start_time form inputs into a datetime object."""

    s_date = request.form.get("start-date", None)
    s_time = request.form.get("start-time", None)

    conv_date = datetime.strptime(s_date, "%Y-%m-%d").date()
    conv_time = datetime.strptime(s_time, "%H:%M").time()

    return datetime.combine(conv_date, conv_time)


def make_end_datetime_obj():
    """Combines end_date and end_time form inputs into a datetime object."""

    e_date = request.form.get("end-date", None)
    e_time = request.form.get("end-time", None)

    conv_date = datetime.strptime(e_date, "%Y-%m-%d").date()
    conv_time = datetime.strptime(e_time, "%H:%M").time()

    return datetime.combine(conv_date, conv_time)


def get_trip_entities(trip):
    """Creates a list of sql objects and sorts them by date"""

    results = trip.flight + trip.hotel + trip.car_rental + trip.public_transportation + trip.event + trip.meeting
    sorted_results = sorted(results, key=attrgetter('starts_at'))
    return sorted_results


def daterange(start_date, end_date):
    """Determines"""
    for n in range(int((end_date - start_date).days)):
        yield start_date + timedelta(n)
