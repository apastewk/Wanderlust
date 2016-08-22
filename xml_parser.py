import xml.etree.ElementTree as ET

from datetime import datetime

################################################################################

def worldmate_xml_parser(xml_data):
    """Find the information that I need in my XML."""

    root = ET.fromstring(fp)

    for result_type in root.iter(result_type):
        if result_type == "flight":
            flight_parser()
        elif result_type == "hotel-reservation":
            hotel_parser()
        elif result_type == "car-rental":
            hotel_parser()
        elif result_type == "public-transporation":
            public_transportation_parser()
        elif result_type == "event":
            event_parser()
        elif result_type == "meeting":
            meeting_parser()


def flight_parser(flights):
    """Parses for flight details."""

    root = ET.fromstring(flights)
    parsed_data = {}

    for flight in root.iter("flight"):

        parsed_data["flight"] = {}

        parsed_data["flight"]["confirmation_num"] = flight.find("provider-details").find("confirmation-number").text
        parsed_data["flight"]["airline"] = flight.find("provider-details").find("name").text
        airline_code = flight.find("details").attrib["airline-code"]
        airline_number = flight.find("details").attrib["number"]
        parsed_data["flight"]["flight_num"] = airline_code + " " + airline_number
        starts_at_xml = flight.find("departure").find("local-date-time").text
        parsed_data["flight"]["starts_at"] = datetime.strptime(starts_at_xml, "%Y-%m-%dT%H:%M:%S.%fZ")
        parsed_data["flight"]["departs_from"] = flight.find("departure").find("name").text
        parsed_data["flight"]["airpt_code_dep"] = flight.find("departure").find("airport-code").text
        ends_at_xml = flight.find("arrival").find("local-date-time").text
        parsed_data["flight"]["ends_at"] = datetime.strptime(ends_at_xml, "%Y-%m-%dT%H:%M:%S.%fZ")
        parsed_data["flight"]["arrives_to"] = flight.find("arrival").find("name").text
        parsed_data["flight"]["airpt_code_arr"] = flight.find("arrival").find("airport-code").text
        parsed_data["flight"]["duration"] = flight.find("duration").text
        parsed_data["flight"]["rewards_num"] = flight.find("traveler").find("loyalty-program").attrib["number"]

    return parsed_data["flight"]


def hotel_parser(hotels):
    """Parses for hotel details."""

    root = ET.fromstring(hotels)
    parsed_data = {}

    for hotel in root.iter("hotel-reservation"):
    
        parsed_data["hotel"] = {}

        parsed_data["hotel"]["confirmation_num"] = hotel.find("booking-details").find("confirmation-number").text
        parsed_data["hotel"]["hotel_name"] = hotel.find("hotel-name").text
        street = hotel.find("address").find("street").text
        city = hotel.find("address").find("city").text
        state_code = hotel.find("address").find("state-code").text
        parsed_data["hotel"]["address"] = street + " " + city + ", " + state_code
        starts_at_xml = hotel.find("check-in").text
        parsed_data["hotel"]["starts_at"] = datetime.strptime(starts_at_xml, "%Y-%m-%d")
        ends_at_xml = hotel.find("check-out").text
        parsed_data["hotel"]["ends_at"] = datetime.strptime(ends_at_xml, "%Y-%m-%d")
        parsed_data["hotel"]["room_type"] = hotel.find("room").text

    return parsed_data["hotel"]


def car_rental_parser(car_rentals):
    """Parses for car rental details."""

    root = ET.fromstring(car-rental)
    parsed_data = {}

    for car_rental in root.iter("car-rental"):
   
        parsed_data["car-rental"] = {}

        parsed_data["car-rental"]["confirmation_num"] = car_rental.find("booking-details").find("confirmation-number").text
        parsed_data["car-rental"]["agency_name"] = car_rental.find("booking-details").find("name").text
        starts_at_xml = car_rental.find("pickup").find("local-date-time").text
        parsed_data["car-rental"]["starts_at"] = datetime.strptime(starts_at_xml, "%Y-%m-%dT%H:%M:%S.%f")
        airport_code_pickup = car_rental.find("pickup").find("airport-code").text
        street_pickup = car_rental.find("pickup").find("address").find("street").text
        city_pickup = car_rental.find("pickup").find("address").find("city").text
        state_code_pickup = car_rental.find("pickup").find("address").find("state-code").text
        parsed_data["car-rental"]["pickup_from"] = airport_code_pickup + " " + street_pickup + " " + city_pickup + " " + state_code_pickup
        ends_at_xml = car_rental.find("dropoff").find("local-date-time").text
        parsed_data["car-rental"]["ends_at"] = datetime.strptime(ends_at_xml, "%Y-%m-%dT%H:%M:%S.%f")
        airport_code_dropoff = car_rental.find("dropoff").find("airport-code").text
        street_dropoff = car_rental.find("dropoff").find("address").find("street").text
        city_dropoff = car_rental.find("dropoff").find("address").find("city").text
        state_code_dropoff = car_rental.find("dropoff").find("address").find("state-code").text
        parsed_data["car-rental"]["dropoff_to"] = airport_code_dropoff + " " + street_dropoff + " " + city_dropoff + " " + state_code_dropoff
        first_name = car_rental.find("driver").find("first-name").text
        last_name = car_rental.find("driver").find("last-name").text
        parsed_data["car-rental"]["drivers_name"] = first_name + " " + last_name
        parsed_data["car-rental"]["car_type"] = car_rental.find("car-type").attrib["name"]
        parsed_data["car-rental"]["rewards_num"] = car_rental.find("driver").find("loyalty-program").attrib["number"]

    return parsed_data["car-rental"]


def public_transportation_parser(public_transportation):
    """Parses for public transportation details."""

    root = ET.fromstring(flights)
    parsed_data = {}

    for public_transportation in root.iter("public-transporation"):

        parsed_data["public-transporation"] = {}

        parsed_data["public-transporation"]["transport_num"] = public_transportation.find("train-number").text
        parsed_data["public-transporation"]["confirmation_num"] = public_transportation.find("booking-details").find("confirmation-number").text
        parsed_data["public-transporation"]["vendor_name"] = public_transportation.find("booking-details").find("name").text
        station_name_dept = public_transportation.find("departure").find("station-name").text
        city_dept = public_transportation.find("departure").find("address").find("city").text
        country_code_dept = public_transportation.find("departure").find("address").find("country-code").text
        parsed_data["public-transporation"]["departs_from"] = station_name_dept + " " + city_dept + ", " + country_code_dept
        starts_at_xml = public_transportation.find("departure").find("local-date-time").text
        parsed_data["public-transporation"]["starts_at"] = datetime.strptime(starts_at_xml, "%Y-%m-%dT%H:%M:%S.%f")
        station_name_arr = public_transportation.find("arrival").find("station-name").text
        city_arr = public_transportation.find("arrival").find("address").find("city").text
        country_code_arr = public_transportation.find("arrival").find("address").find("country-code").text
        parsed_data["public-transporation"]["arrives_to"] = station_name_arr + " " + city_arr + " " + country_code_arr
        ends_at_xml = public_transportation.find("arrival").find("local-date-time").text
        parsed_data["public-transporation"]["ends_at"] = datetime.strptime(ends_at_xml, "%Y-%m-%dT%H:%M:%S.%f")
        first_name = public_transportation.find("traveler").find("first-name").text
        last_name = public_transportation.find("traveler").find("last-name").text
        parsed_data["public-transporation"]["travelers_name"] = first_name + " " + last_name
        parsed_data["public-transporation"]["duration"] = public_transportation.find("duration").text

    return parsed_data["public-transporation"]


def event_parser(event):
    """Parses for event details."""

    root = ET.fromstring(event)
    parsed_data = {}

    for event in root.iter("event"):

        parsed_data["event"] = {}

        parsed_data["event"]["confirmation_num"] = event.find("booking-details").find("confirmation-number").text
        parsed_data["event"]["event_name"] = event.find("event-name").text
        starts_at_xml = event.find("local-start-time").text
        parsed_data["event"]["starts_at"] = datetime.strptime(starts_at_xml, "%Y-%m-%dT%H:%M:%S.%f")
        location = event.find("location").text
        street = event.find("address").find("street").text
        city = event.find("address").find("city").text
        state_code = event.find("address").find("state-code").text
        parsed_data["event"]["address"] = location + " " + street + " " + city + ", " + state_code

    return parsed_data["event"]


def meeting_parser(meeting):
    """Parses for meeting details."""

    root = ET.fromstring(meeting)
    parsed_data = {}

    for meeting in root.iter("meeting"):

        parsed_data["meeting"] = {}

        parsed_data["meeting"]["meeting_subject"] = meeting.find("name").text
        starts_at_xml = meeting.find("local-start-time").text
        parsed_data["meeting"]["starts_at"] = datetime.strptime(starts_at_xml, "%Y-%m-%dT%H:%M:%S.%f")
        location = meeting.find("location").text
        street = meeting.find("address").find("street").text
        city = meeting.find("address").find("city").text
        state_code = meeting.find("address").find("state-code").text
        parsed_data["meeting"]["address"] = location + " " + street + " " + city + " " + state_code

    return parsed_data["meeting"]
