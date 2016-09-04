from operator import attrgetter
from datetime import datetime
import hashlib
from model import Trip
# from xml_parser import worldmate_xml_parser, user_parser
# from service import identify_email_type, identify_users_trip, create_item

################################################################################


def hash_password(password):
    """Hashes a users password.

        >>> hash_password('123456')
        'f8cdb04495ded4761525'
    """

     # salt = uuid.uuid4().hex
    return hashlib.sha224(password).hexdigest()[:20]


def make_datetime_obj(date, time):
    """Combines start_date and start_time form inputs into a datetime object.

        >>> make_datetime_obj('2016-08-26', '18:00')
        datetime.datetime(2016, 8, 26, 18, 0)

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
    """Converts a list of trip entities into a modified dictionary.

        >>> e1 = Event(event_name = 'Hackbright', starts_at = datetime(2016, 9, 14, 0, 0, 0))
        >>> m1 = Meeting(meeting_subject = 'Go Karting', starts_at = datetime(2016, 9, 14, 5, 0, 0))
        >>> trip_entities = [e1, m1]
        >>> create_trip_entities_dict(trip_entities)
        [{'event_name': 'Hackbright', 'starts_at': 'Wed, Sep 14, 2016', 'start_time': '00:00'}, {'meeting_subject': 'Go Karting', 'start_time': '05:00', 'starts_at': 'Thu, Sep 29, 2016'}]
    """

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
    """Modifies a users trip start_date and end_date.

        >>> trips = [Trip(user_id=1, trip_id=1, start_date=datetime.strptime("2016-08-10 00:00:00", "%Y-%m-%d %H:%M:%S"), end_date=datetime.strptime("2016-09-20 00:00:00", "%Y-%m-%d %H:%M:%S"), trip_name="Rome", destination="Rome")]
        >>> modifies_user_trips(trips)
        [('Rome', 'Wed, Aug 10, 2016', 'Tue, Sep 20, 2016', None, 1)]
    """

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


# def xml_helper_functions(xml_string):

#     start_date, parsed_data = worldmate_xml_parser(xml_string)

#     user_email = user_parser(xml_string)

#     trip_id = identify_users_trip(start_date, user_email)

#     item_type, item_data = identify_email_type(parsed_data)

#     create_item(item_type, item_data, trip_id)


if __name__ == "__main__":
    import doctest

    print
    result = doctest.testmod()
    if not result.failed:
        print "ALL TESTS PASSED. GOOD WORK!"
    print


