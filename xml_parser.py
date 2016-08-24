import xml.etree.ElementTree as ET

from datetime import datetime

################################################################################

def worldmate_xml_parser(xml_string):
    """Identifies which type of data is in XML and pases it to the appropriate parser."""

    root = ET.fromstring(xml_string)

    event = ["flight",
              "hotel-reservation",
              "car-rental", 
              "public-transporation",
              "event",
              "meeting"]

    # confirmations = {"event": event_parser,
    #                  "flight": flight_parser,
    #                  "hotel-reservation": hotel_parser,
    #                  "car-rental": car_rental_parser,
    #                  "public-transportation": public_transportation_parser,
    #                  "meeting": meeting_parser}

    for result_type in event:
        for item in root.iter("items"):
            if item.find(result_type) is not None:
                if result_type == "flight":
                    flight_parser(xml_string)
                elif result_type == "hotel-reservation":
                    hotel_parser(xml_string)
                elif result_type == "car-rental":
                    car_rental_parser(xml_string)
                elif result_type == "public-transporation":
                    public_transportation_parser(xml_string)
                elif result_type == "event":
                    event_parser(xml_string)
                elif result_type == "meeting":
                    meeting_parser(xml_string)
            print result_type


def flight_parser(flights):
    """Parses for flight details."""

    root = ET.fromstring(flights)
    parsed_data = {}

    for flight in root.iter("flight"):

        parsed_data["flight"] = {}

        provider_details = flight.find("provider-details")
        details = flight.find("details")
        departure = flight.find("departure")
        arrival = flight.find("arrival")
        traveler = flight.find("traveler")

        parsed_data["flight"]["confirmation_num"] = provider_details.findtext("confirmation-number", default=None)
        parsed_data["flight"]["airline"] = provider_details.findtext("name", default=None)
        parsed_data["flight"]["flight_num"] = None
        if details:
            airline_code = details.attrib["airline-code"]
            airline_number = details.attrib["number"]
            parsed_data["flight"]["flight_num"] = airline_code + " " + airline_number
        starts_at_xml = departure.findtext("local-date-time", default=None)
        parsed_data["flight"]["starts_at"] = datetime.strptime(starts_at_xml, "%Y-%m-%dT%H:%M:%S.%fZ")
        parsed_data["flight"]["departs_from"] = departure.findtext("name", default=None)
        parsed_data["flight"]["airpt_code_dep"] = departure.findtext("airport-code", default=None)
        ends_at_xml = arrival.find("local-date-time").text
        parsed_data["flight"]["ends_at"] = datetime.strptime(ends_at_xml, "%Y-%m-%dT%H:%M:%S.%fZ")
        parsed_data["flight"]["arrives_to"] = arrival.findtext("name", default=None)
        parsed_data["flight"]["airpt_code_arr"] = arrival.findtext("airport-code", default=None)
        parsed_data["flight"]["duration"] = flight.findtext("duration", default=None)
        parsed_data["flight"]["rewards_num"] = None
        if traveler.find("loyalty-program"):
            parsed_data["flight"]["rewards_num"] = traveler.find("loyalty-program").attrib["number"]

    return parsed_data["flight"]


def hotel_parser(hotels):
    """Parses for hotel details."""

    root = ET.fromstring(hotels)
    parsed_data = {}

    for hotel in root.iter("hotel-reservation"):
    
        parsed_data["hotel"] = {}

        booking_details = hotel.find("booking-details")
        address = hotel.find("address")

        parsed_data["hotel"]["confirmation_num"] = booking_details.findtext("confirmation-number", default=None)
        parsed_data["hotel"]["hotel_name"] = hotel.findtext("hotel-name", default=None)
        street = address.findtext("street", default=None)
        city = address.findtext("city", default=None)
        state_code = address.findtext("state-code", default=None)
        parsed_data["hotel"]["address"] = street + " " + city + ", " + state_code
        starts_at_xml = hotel.findtext("check-in", default=None)
        parsed_data["hotel"]["starts_at"] = datetime.strptime(starts_at_xml, "%Y-%m-%d")
        ends_at_xml = hotel.findtext("check-out", default=None)
        parsed_data["hotel"]["ends_at"] = datetime.strptime(ends_at_xml, "%Y-%m-%d")
        parsed_data["hotel"]["room_type"] = hotel.findtext("room", default=None)

    return parsed_data["hotel"]


def car_rental_parser(car_rentals):
    """Parses for car rental details."""

    root = ET.fromstring(car_rentals)
    parsed_data = {}

    for car_rental in root.iter("car-rental"):

        parsed_data["car-rental"] = {}

        booking_details = car_rental.find("booking-details")
        pickup = car_rental.find("pickup")
        dropoff = car_rental.find("dropoff")
        driver = car_rental.find("driver")
        car_type = car_rental.find("car-type")

        parsed_data["car-rental"]["confirmation_num"] = booking_details.findtext("confirmation-number", default=None)
        parsed_data["car-rental"]["agency_name"] = booking_details.findtext("name", default=None)
        starts_at_xml = pickup.findtext("local-date-time", default=None)
        parsed_data["car-rental"]["starts_at"] = datetime.strptime(starts_at_xml, "%Y-%m-%dT%H:%M:%S.%f")
        airport_code_pickup = pickup.findtext("airport-code", default=None)
        street_pickup = pickup.find("address").findtext("street", default=None)
        city_pickup = pickup.find("address").findtext("city", default=None)
        state_code_pickup = pickup.find("address").findtext("state-code", default=None)
        parsed_data["car-rental"]["pickup_from"] = airport_code_pickup + " " + street_pickup + " " + city_pickup + " " + state_code_pickup
        ends_at_xml = car_rental.find("dropoff").findtext("local-date-time", default=None)
        parsed_data["car-rental"]["ends_at"] = datetime.strptime(ends_at_xml, "%Y-%m-%dT%H:%M:%S.%f")
        airport_code_dropoff = dropoff.findtext("airport-code", default=None)
        street_dropoff = dropoff.find("address").findtext("street", default=None)
        city_dropoff = dropoff.find("address").findtext("city", default=None)
        state_code_dropoff = dropoff.find("address").findtext("state-code", default=None)
        parsed_data["car-rental"]["dropoff_to"] = airport_code_dropoff + " " + street_dropoff + " " + city_dropoff + " " + state_code_dropoff
        first_name = driver.findtext("first-name", default=None)
        last_name = driver.findtext("last-name", default=None)
        parsed_data["car-rental"]["drivers_name"] = first_name + " " + last_name
        parsed_data["car-rental"]["car_type"] = None
        if car_type:
            parsed_data["car-rental"]["car_type"] = car_type.attrib["name"]
        parsed_data["car-rental"]["rewards_num"] = None
        if driver.find("loyalty-program"):
            parsed_data["car-rental"]["rewards_num"] = driver.find("loyalty-program").attrib["number"]

    return parsed_data["car-rental"]


def public_transportation_parser(public_transportation):
    """Parses for public transportation details."""

    root = ET.fromstring(public_transportation)
    parsed_data = {}

    for public_transportation in root.iter("public-transporation"):

        parsed_data["public-transporation"] = {}

        booking_details = public_transportation.find("booking-details")
        departure = public_transportation.find("departure")
        arrival = public_transportation.find("arrival")
        traveler = public_transportation.find("traveler")

        parsed_data["public-transporation"]["transport_num"] = public_transportation.findtext("train-number", default=None)
        parsed_data["public-transporation"]["confirmation_num"] = booking_details.findtext("confirmation-number", default=None)
        parsed_data["public-transporation"]["vendor_name"] = booking_details.findtext("name", default=None)
        station_name_dept = departure.findtext("station-name", default=None)
        city_dept = departure.find("address").findtext("city", default=None)
        country_code_dept = departure.find("address").findtext("country-code", default=None)
        parsed_data["public-transporation"]["departs_from"] = station_name_dept + " " + city_dept + ", " + country_code_dept
        starts_at_xml = departure.findtext("local-date-time", default=None)
        parsed_data["public-transporation"]["starts_at"] = datetime.strptime(starts_at_xml, "%Y-%m-%dT%H:%M:%S.%f")
        station_name_arr = arrival.findtext("station-name", default=None)
        city_arr = arrival.find("address").findtext("city", default=None)
        country_code_arr = arrival.find("address").findtext("country-code", default=None)
        parsed_data["public-transporation"]["arrives_to"] = station_name_arr + " " + city_arr + " " + country_code_arr
        ends_at_xml = arrival.findtext("local-date-time", default=None)
        parsed_data["public-transporation"]["ends_at"] = datetime.strptime(ends_at_xml, "%Y-%m-%dT%H:%M:%S.%f")
        first_name = traveler.findtext("first-name", default=None)
        last_name = traveler.findtext("last-name", default=None)
        parsed_data["public-transporation"]["travelers_name"] = first_name + " " + last_name
        parsed_data["public-transporation"]["duration"] = public_transportation.findtext("duration", default=None)

    return parsed_data["public-transporation"]


def event_parser(event):
    """Parses for event details."""

    root = ET.fromstring(event)
    parsed_data = {}

    for event in root.iter("event"):

        parsed_data["event"] = {}

        booking_details = event.find("booking-details")
        address = event.find("address")

        parsed_data["event"]["confirmation_num"] = booking_details.findtext("confirmation-number", default=None)
        parsed_data["event"]["event_name"] = event.findtext("event-name", default=None)
        starts_at_xml = event.findtext("local-start-time", default=None)
        parsed_data["event"]["starts_at"] = datetime.strptime(starts_at_xml, "%Y-%m-%dT%H:%M:%S.%f")
        location = event.findtext("location", default=None)
        street = address.findtext("street", default=None)
        city = address.findtext("city", default=None)
        state_code = address.findtext("state-code", default=None)
        parsed_data["event"]["address"] = location + " " + street + " " + city + ", " + state_code

    return parsed_data["event"]


def meeting_parser(meeting):
    """Parses for meeting details."""

    root = ET.fromstring(meeting)
    parsed_data = {}

    for meeting in root.iter("meeting"):

        parsed_data["meeting"] = {}

        address = meeting.find("address")

        parsed_data["meeting"]["meeting_subject"] = meeting.findtext("name", default=None)
        starts_at_xml = meeting.findtext("local-start-time", default=None)
        parsed_data["meeting"]["starts_at"] = datetime.strptime(starts_at_xml, "%Y-%m-%dT%H:%M:%S.%f")
        location = meeting.findtext("location", default=None)
        street = address.findtext("street", default=None)
        city = address.findtext("city", default=None)
        state_code = address.findtext("state-code", default=None)
        parsed_data["meeting"]["address"] = location + " " + street + " " + city + " " + state_code

    return parsed_data["meeting"]
