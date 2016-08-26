from model import User, Trip, Event, Flight, Hotel, CarRental, Meeting
from model import PublicTransportation, db
from sqlalchemy import and_
from utility import make_datetime_obj
from flask import session, flash

################################################################################


def signup(firstname, lastname, email, hashed_password):
    """
    Gather information submitted in signup form, store in database and redirect
    to users trip page.
    """

    if User.query.filter(User.email == email).first():
        flash("That email is already registered.  Please log in or choose a different email.")
    else:
        new_user = User(email=email,
                        firstname=firstname,
                        lastname=lastname,
                        password=hashed_password)

        db.session.add(new_user)
        db.session.commit()
        flash("You are now registered! Please login.")


def check_login(email, hashed_password):
    """
    Verifies that the users email is in the database and that the password matches
    the email. If verification passes, redirects to users trip page.
    """

    check_email = User.query.filter(User.email == email).first()

    if check_email:
        if check_email.password == hashed_password:
            session["logged_in"] = email
            return True
        else:
            flash("The email and password you entered do not match our records.")
    else:
        flash("The email you entered does not exist in our records.")
        return False


def retrieves_user_trips(session_user_id):
    """Accesses all of the trips associated with a user."""

    trips_list = []

    all_trips = Trip.query.filter(Trip.user_id == session_user_id).order_by(Trip.start_date).all()

    for trip in all_trips:
        if trip:
            start_date = trip.start_date.strftime("%a, %b %d, %Y")
            end_date = trip.end_date.strftime("%a, %b %d, %Y")
            trip_detail = (trip.trip_name, start_date, end_date, trip.notes, trip.trip_id)
            trips_list.append(trip_detail)
            return trips_list
        else:
            return None


def add_new_trip_to_db(destination, trip_name, start_date, end_date, notes):
    """Creates a new trip and stores in database."""

    current_user = User.query.filter(User.email == session['logged_in']).first()
    user_id = current_user.user_id

    new_trip = Trip(user_id=user_id,
                    destination=destination,
                    trip_name=trip_name,
                    start_date=start_date,
                    end_date=end_date,
                    notes=notes)

    db.session.add(new_trip)
    db.session.commit()


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


def identify_email_type(parsed_data, trip_id):
    """Identifies type of email and the data the will be put in the database."""

    email_type = parsed_data.keys()[0]

    item_data = parsed_data[email_type]

    create_item(email_type, item_data, trip_id)


def identify_users_trip(start_date, user_email):
    """Identifies the trip of a user that the email is related to."""

    user = User.query.filter(User.email == user_email).first()
    if user is not None:
        user_id = user.user_id

    trip = Trip.query.filter(and_(Trip.start_date <= start_date, Trip.end_date >= start_date, Trip.user_id == user_id)).first()
 
    if trip is not None:
        return trip.trip_id


def create_item(item_type, item_data, trip_id):
    """Adds details related to a particular trip to the database."""

    router_map = {"event": Event,
                  "flight": Flight,
                  "hotel": Hotel,
                  "car-rental": CarRental,
                  "public-transportation": PublicTransportation,
                  "meeting": Meeting}

    if item_type in router_map:
        instance = router_map[item_type]()

    for key in item_data:
        if item_data[key]:
            if key == "start-date":
                instance.starts_at = make_datetime_obj(item_data["start-date"], item_data["start-time"])
            elif key == "end-date":
                instance.ends_at = make_datetime_obj(item_data["end-date"], item_data["end-time"])
            elif key == "start-time" or key == "end-time":
                continue
            else:
                setattr(instance, key, item_data[key])

    instance.trip_id = trip_id

    db.session.add(instance)
    db.session.commit()

