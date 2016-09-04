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


def identify_email_type(parsed_data):
    """Identifies type of email and the data the will be put in the database.

        >>> parsed_data = {'airpt_code_arr': 'YYC', 'type': 'flight'}
        >>> identify_email_type(parsed_data)
        ('flight', {'airpt_code_arr': 'YYC'})
    """

    email_type = parsed_data["type"]
    del parsed_data["type"]
    item_data = parsed_data

    return (email_type, item_data)


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
                print type(item_data["start-date"])
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



if __name__ == "__main__":
    import doctest

    print
    result = doctest.testmod()
    if not result.failed:
        print "ALL TESTS PASSED. GOOD WORK!"
    print


