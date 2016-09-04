"""User Trips"""

from flask import Flask, render_template, redirect, request, flash, session
from model import connect_to_db, User, Trip
from utility import hash_password, get_trip_entities, modifies_user_trips
from utility import create_trip_entities_dict, count_user_trips
from service import create_item, check_login, signup, add_new_trip_to_db
from service import identify_users_trip, identify_email_type
from xml_parser import worldmate_xml_parser, user_parser


app = Flask(__name__)

app.secret_key = "ABC"


################################################################################


@app.route("/")
def homepage():
    """Displays the homepage."""
    return render_template("home.html")


@app.route("/signup", methods=["POST"])
def sign_up():
    """
    Gather information submitted in signup form, store in database and redirect
    to users trip page.
    """

    firstname = request.form.get("firstname")
    lastname = request.form.get("lastname")
    email = request.form.get("email")
    password = request.form.get("password")

    # salt = uuid.uuid4().hex
    hashed_password = hash_password(password)

    signup(firstname, lastname, email, hashed_password)

    return redirect("/")


@app.route("/login", methods=["POST"])
def login():
    """
    Verifies that the users email is in the database and that the password matches
    the email.  If verification passes, redirects to users trip page.
    """

    email = request.form.get("email")
    password = request.form.get("password")

    hashed_password = hash_password(password)

    login = check_login(email, hashed_password)

    if login:
        return redirect("/my_trips")
    else:
        return redirect("/")


@app.route("/logout")
def logout():
    """Logout of trips application."""

    session["logged_in"] = None

    flash("You are now logged out.")

    return redirect("/")


@app.route("/my_trips")
def all_trips():
    """Lists all of the users future and past trips."""

    if session['logged_in']:
        current_user = User.query.filter(User.email == session['logged_in']).first()
        session_user_id = current_user.user_id
    else:
        redirect("/login ")

    trip_count = count_user_trips(session_user_id)

    past_trips = modifies_user_trips(trip_count[1][1])
    
    future_trips = modifies_user_trips(trip_count[1][0])

    return render_template("all_trips.html",
                            trip_count=trip_count,
                            past_trips=past_trips,
                            future_trips=future_trips)


@app.route("/my_trips", methods=["POST"])
def add_new_trip():
    """Creates a new trip."""

    notes = None

    destination = request.form.get("destination")
    trip_name = request.form.get("tripname")
    start_date = request.form.get("startdate")
    end_date = request.form.get("enddate")
    notes = request.form.get("notes")

    add_new_trip_to_db(destination, trip_name, start_date, end_date, notes)

    return redirect("/my_trips")


@app.route("/my_trips/<trip_id>")
def trip_details(trip_id):
    """Lists in chronological order a trips particulars."""

    trip = Trip.query.filter(Trip.trip_id == trip_id).first()
    trip_name = trip.trip_name
    destination = trip.destination

    # start_date = trip.start_date
    # end_date = trip.end_date

    # range_of_dates = []

    # for single_date in daterange(start_date, end_date):
    #     conv_single_date = single_date.strftime("%a, %b %d, %Y")
    #     range_of_dates.append(conv_single_date)

    # flickr.flickr_search(destination)

    trip_entities = get_trip_entities(trip)

    trip_entities = create_trip_entities_dict(trip_entities)

    return render_template("trip_details.html",
                            trip_id=trip_id,
                            trip_name=trip_name,
                            trip_entities=trip_entities,
                            destination=destination)


@app.route("/my_trips/<trip_id>", methods=["POST"])
def add_form_trip_details(trip_id):
    """Adds the newly submitted confirmation trip details to the database."""

    form_type = request.form.get("ftype", None)

    create_item(form_type, request.form, trip_id)

    return redirect("/my_trips/" + trip_id)


@app.route("/incoming_xml", methods=["POST"])
def process_incoming_xml():
    """Parses email XML and adds the parsed email trip details to the database."""

    xml_string = request.data

    start_date, parsed_data = worldmate_xml_parser(xml_string)

    user_email = user_parser(xml_string)

    trip_id = identify_users_trip(start_date, user_email)

    item_type, item_data = identify_email_type(parsed_data)

    create_item(item_type, item_data, trip_id)


    ############################################################################


if __name__ == "__main__":

    connect_to_db(app)

    app.run(debug=True, host='0.0.0.0')
