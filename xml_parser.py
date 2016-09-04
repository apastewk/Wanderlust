import xml.etree.ElementTree as ET
from service import identify_email_type, identify_users_trip
from datetime import datetime


################################################################################


def worldmate_xml_parser(xml_string):
    """Identifies which type of data is in XML and pases it to the appropriate parser.

    """

    root = ET.fromstring(xml_string)

    event = ["flight",
             "hotel-reservation",
             "car-rental",
             "public-transporation",
             "event",
             "meeting"]

    for result_type in event:
        for item in root.iter("items"):
            if item.find(result_type) is not None:
                if result_type == "flight":
                    parsed_xml = flight_parser(root)
                elif result_type == "hotel-reservation":
                    parsed_xml = hotel_parser(root)
                elif result_type == "car-rental":
                    parsed_xml = car_rental_parser(root)
                elif result_type == "public-transporation":
                    parsed_xml = public_transportation_parser(root)
                elif result_type == "event":
                    parsed_xml = event_parser(root)
                elif result_type == "meeting":
                    parsed_xml = meeting_parser(root)

  # confirmations = {"event": event_parser,
  #                    "flight": flight_parser,
  #                    "hotel-reservation": hotel_parser,
  #                    "car-rental": car_rental_parser,
  #                    "public-transportation": public_transportation_parser,
  #                    "meeting": meeting_parser}

    return parsed_xml

def user_parser(xml_string):
    """Parses for user details.

        >>> user_parser(<Element '{http://www.worldmate.com/schemas/worldmate-api-v1.xsd}worldmate-parsing-result' at 0x7fc4a9dfded0>)
        "allison.pastewka@gmail.com"
    """

    root = ET.fromstring(xml_string)

    user_email = None

    for flight in root.iter("end-user-emails"):
        user = flight.find("user")
        if user is not None:
            user_email = user.attrib["email"]

    return user_email


def flight_parser(root):
    """Parses for flight details.

        >>> xml_string = open("xml_string.txt").read()
        >>> root = ET.fromstring(xml_string)
        >>> flight_parser(root)
        {{'ends_at': datetime.datetime(2017, 5, 25, 17, 40), 'arrives_to': \
        'Calgary International Airport', 'flight_num': 'WS 1509', 'confirmation_num': \
        'UYWJAC', 'departs_from': 'SFO International Airport', 'airpt_code_dep': 'SFO', \
        'duration': '160', 'airline': 'WestJet', 'rewards_num': '115343480', \
        'starts_at': datetime.datetime(2017, 5, 25, 14, 0), 'airpt_code_arr': 'YYC', \
        'type': 'flight'}, {'ends_at': datetime.datetime(2017, 5, 31, 13, 12), \
        'arrives_to': 'SFO International Airport', 'flight_num': 'WS 1508', \
        'confirmation_num': 'UYWJAC', 'departs_from': 'Calgary International Airport', \
        'airpt_code_dep': 'YYC', 'duration': '172', 'airline': 'WestJet', 'rewards_num': \
        '115343480', 'starts_at': datetime.datetime(2017, 5, 31, 11, 20), \
        'airpt_code_arr': 'SFO', 'type': 'flight'}}
    """

    parsed_data = {}

    for flight in root.iter("flight"):

        provider_details = flight.find("provider-details")
        details = flight.find("details")
        departure = flight.find("departure")
        arrival = flight.find("arrival")
        traveler = flight.find("traveler")

        parsed_data["confirmation_num"] = provider_details.findtext("confirmation-number", default=None)
        parsed_data["airline"] = provider_details.findtext("name", default=None)
        parsed_data["flight_num"] = None
        if details is not None:
            airline_code = details.attrib["airline-code"]
            airline_number = details.attrib["number"]
            parsed_data["flight_num"] = airline_code + " " + airline_number
        starts_at_xml = departure.findtext("local-date-time", default=None)
        parsed_data["starts_at"] = datetime.strptime(starts_at_xml, "%Y-%m-%dT%H:%M:%S.%fZ")
        parsed_data["departs_from"] = departure.findtext("name", default=None)
        parsed_data["airpt_code_dep"] = departure.findtext("airport-code", default=None)
        ends_at_xml = arrival.find("local-date-time").text
        parsed_data["ends_at"] = datetime.strptime(ends_at_xml, "%Y-%m-%dT%H:%M:%S.%fZ")
        parsed_data["arrives_to"] = arrival.findtext("name", default=None)
        parsed_data["airpt_code_arr"] = arrival.findtext("airport-code", default=None)
        parsed_data["duration"] = flight.findtext("duration", default=None)
        parsed_data["rewards_num"] = None
        if traveler.find("loyalty-program") is not None:
            parsed_data["rewards_num"] = traveler.find("loyalty-program").attrib["number"]
        parsed_data["type"] = "flight"
        
    return (parsed_data["starts_at"], parsed_data)


def hotel_parser(root):
    """Parses for hotel details."""

    parsed_data = {}

    for hotel in root.iter("hotel-reservation"):

        booking_details = hotel.find("booking-details")
        address = hotel.find("address")

        parsed_data["confirmation_num"] = booking_details.findtext("confirmation-number", default=None)
        parsed_data["hotel_name"] = hotel.findtext("hotel-name", default=None)
        street = address.findtext("street", default=None)
        city = address.findtext("city", default=None)
        state_code = address.findtext("state-code", default=None)
        parsed_data["address"] = street + " " + city + ", " + state_code
        starts_at_xml = hotel.findtext("check-in", default=None)
        parsed_data["starts_at"] = datetime.strptime(starts_at_xml, "%Y-%m-%d")
        ends_at_xml = hotel.findtext("check-out", default=None)
        parsed_data["ends_at"] = datetime.strptime(ends_at_xml, "%Y-%m-%d")
        parsed_data["room_type"] = hotel.findtext("room", default=None)
        parsed_data["type"] = "hotel"

    return (parsed_data["starts_at"], parsed_data)


def car_rental_parser(root):
    """Parses for car rental details."""

    parsed_data = {}

    for car_rental in root.iter("car-rental"):

        booking_details = car_rental.find("booking-details")
        pickup = car_rental.find("pickup")
        dropoff = car_rental.find("dropoff")
        driver = car_rental.find("driver")
        car_type = car_rental.find("car-type")

        parsed_data["confirmation_num"] = booking_details.findtext("confirmation-number", default=None)
        parsed_data["agency_name"] = booking_details.findtext("name", default=None)
        starts_at_xml = pickup.findtext("local-date-time", default=None)
        parsed_data["starts_at"] = datetime.strptime(starts_at_xml, "%Y-%m-%dT%H:%M:%S.%f")
        airport_code_pickup = pickup.findtext("airport-code", default=None)
        street_pickup = pickup.find("address").findtext("street", default=None)
        city_pickup = pickup.find("address").findtext("city", default=None)
        state_code_pickup = pickup.find("address").findtext("state-code", default=None)
        parsed_data["pickup_from"] = airport_code_pickup + " " + street_pickup + " " + city_pickup + " " + state_code_pickup
        ends_at_xml = car_rental.find("dropoff").findtext("local-date-time", default=None)
        parsed_data["ends_at"] = datetime.strptime(ends_at_xml, "%Y-%m-%dT%H:%M:%S.%f")
        airport_code_dropoff = dropoff.findtext("airport-code", default=None)
        street_dropoff = dropoff.find("address").findtext("street", default=None)
        city_dropoff = dropoff.find("address").findtext("city", default=None)
        state_code_dropoff = dropoff.find("address").findtext("state-code", default=None)
        parsed_data["dropoff_to"] = airport_code_dropoff + " " + street_dropoff + " " + city_dropoff + " " + state_code_dropoff
        first_name = driver.findtext("first-name", default=None)
        last_name = driver.findtext("last-name", default=None)
        parsed_data["drivers_name"] = first_name + " " + last_name
        parsed_data["car_type"] = None
        if car_type is not None:
            parsed_data["car_type"] = car_type.attrib["name"]
        parsed_data["rewards_num"] = None
        if driver.find("loyalty-program") is not None:
            parsed_data["rewards_num"] = driver.find("loyalty-program").attrib["number"]
        parsed_data["type"] = "car-rental"

    return (parsed_data["starts_at"], parsed_data)


def public_transportation_parser(root):
    """Parses for public transportation details."""

    parsed_data = {}

    for public_transportation in root.iter("public-transporation"):

        booking_details = public_transportation.find("booking-details")
        departure = public_transportation.find("departure")
        arrival = public_transportation.find("arrival")
        traveler = public_transportation.find("traveler")

        parsed_data["transport_num"] = public_transportation.findtext("train-number", default=None)
        parsed_data["confirmation_num"] = booking_details.findtext("confirmation-number", default=None)
        parsed_data["vendor_name"] = booking_details.findtext("name", default=None)
        station_name_dept = departure.findtext("station-name", default=None)
        city_dept = departure.find("address").findtext("city", default=None)
        country_code_dept = departure.find("address").findtext("country-code", default=None)
        parsed_data["departs_from"] = station_name_dept + " " + city_dept + ", " + country_code_dept
        starts_at_xml = departure.findtext("local-date-time", default=None)
        parsed_data["starts_at"] = datetime.strptime(starts_at_xml, "%Y-%m-%dT%H:%M:%S.%f")
        station_name_arr = arrival.findtext("station-name", default=None)
        city_arr = arrival.find("address").findtext("city", default=None)
        country_code_arr = arrival.find("address").findtext("country-code", default=None)
        parsed_data["arrives_to"] = station_name_arr + " " + city_arr + " " + country_code_arr
        ends_at_xml = arrival.findtext("local-date-time", default=None)
        parsed_data["ends_at"] = datetime.strptime(ends_at_xml, "%Y-%m-%dT%H:%M:%S.%f")
        first_name = traveler.findtext("first-name", default=None)
        last_name = traveler.findtext("last-name", default=None)
        parsed_data["travelers_name"] = first_name + " " + last_name
        parsed_data["duration"] = public_transportation.findtext("duration", default=None)
        parsed_data["type"] = "public-transportation"

    return (parsed_data["starts_at"], parsed_data)


def event_parser(root):
    """Parses for event details."""

    parsed_data = {}

    for event in root.iter("event"):

        booking_details = event.find("booking-details")
        address = event.find("address")

        parsed_data["confirmation_num"] = booking_details.findtext("confirmation-number", default=None)
        parsed_data["event_name"] = event.findtext("event-name", default=None)
        starts_at_xml = event.findtext("local-start-time", default=None)
        parsed_data["starts_at"] = datetime.strptime(starts_at_xml, "%Y-%m-%dT%H:%M:%S.%f")
        location = event.findtext("location", default=None)
        street = address.findtext("street", default=None)
        city = address.findtext("city", default=None)
        state_code = address.findtext("state-code", default=None)
        parsed_data["address"] = location + " " + street + " " + city + ", " + state_code
        parsed_data["type"] = "event"

    return (parsed_data["starts_at"], parsed_data)


def meeting_parser(root):
    """Parses for meeting details."""

    parsed_data = {}

    for meeting in root.iter("meeting"):

        address = meeting.find("address")

        parsed_data["meeting_subject"] = meeting.findtext("name", default=None)
        starts_at_xml = meeting.findtext("local-start-time", default=None)
        parsed_data["starts_at"] = datetime.strptime(starts_at_xml, "%Y-%m-%dT%H:%M:%S.%f")
        location = meeting.findtext("location", default=None)
        street = address.findtext("street", default=None)
        city = address.findtext("city", default=None)
        state_code = address.findtext("state-code", default=None)
        parsed_data["address"] = location + " " + street + " " + city + " " + state_code
        parsed_data["type"] = "meeting"

    return (parsed_data["starts_at"], parsed_data)
