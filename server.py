"""User Trips"""

import os

from flask import Flask, render_template, redirect, request, flash, session

from model import User, Trip, Flight, Hotel, CarRental, PublicTransportation
from model import Meeting, Event, connect_to_db, db
from utility import make_start_datetime_obj, make_end_datetime_obj, get_trip_entities
from utility import daterange
from xml_parser import worldmate_xml_parser

from datetime import datetime, timedelta, date
import psycopg2

import hashlib, uuid


app = Flask(__name__)

app.secret_key = "ABC"


################################################################################


@app.route("/")
def homepage():
    """Displays the homepage."""

    return render_template("home.html")


@app.route("/signup")
def sign_up_form():
    """Displays a sign up form."""

    return render_template("signup_form.html")


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
    hashed_password = hashlib.sha224(password).hexdigest()[:20]

    if User.query.filter(User.email == email).first():
        flash("That email is already registered.  Please log in or choose a different email.")
        return redirect("/signup")
    else:
        new_user = User(email=email,
                        firstname=firstname,
                        lastname=lastname,
                        password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        flash("You are now registered! Please login.")
        return redirect("/login")


@app.route("/login")
def login_form():
    """Displays a login form."""

    return render_template("login_form.html")


@app.route("/login", methods=["POST"])
def login():
    """
    Verifies that the users email is in the database and that the password matches
    the email.  If verification passes, redirects to users trip page.
    """

    email = request.form.get("email")
    password = request.form.get("password")

    # salt = uuid.uuid4().hex
    hashed_password = hashlib.sha224(password).hexdigest()[:20]
    check_email = User.query.filter(User.email == email).first()

    if check_email:
        if check_email.password == hashed_password:
            session["logged_in"] = email
            return redirect("/my_trips")
        else:
            flash("The email and password you entered do not match our records.")
            return redirect("/login")
    else:
        flash("The email you entered does not exist in our records.")
        return redirect("/login")


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

    trips_list = []

    all_trips = Trip.query.filter(Trip.user_id == session_user_id).order_by(Trip.start_date).all()

    for trip in all_trips:
        start_date = trip.start_date.strftime("%a, %b %d, %Y")
        end_date = trip.end_date.strftime("%a, %b %d, %Y")
        trip_detail = (trip.trip_name, start_date, end_date, trip.notes, trip.trip_id)
        trips_list.append(trip_detail)

    return render_template("all_trips.html",
                            trips=trips_list)


@app.route("/add_new_trip")
def add_new_trip_form():
    """User can create a new trip."""

    return render_template("add_new_trip_form.html")


@app.route("/my_trips", methods=["POST"])
def add_new_trip():
    """Creates a new trip."""

    notes = None

    destination = request.form.get("destination")
    trip_name = request.form.get("tripname")
    start_date = request.form.get("startdate")
    end_date = request.form.get("enddate")
    notes = request.form.get("notes")

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
    flash("You have successfully created a new trip!")

    return redirect("/my_trips")


@app.route("/my_trips/<trip_id>")
def trip_details(trip_id):
    """Lists in chronological order a trips particulars."""

    trip = Trip.query.filter(Trip.trip_id == trip_id).first()
    trip_name = trip.trip_name

    start_date = trip.start_date
    end_date = trip.end_date

    daterange(start_date, end_date)

    range_of_dates = []

    for single_date in daterange(start_date, end_date):
        conv_single_date = single_date.strftime("%a, %b %d, %Y")
        range_of_dates.append(conv_single_date)

    trip_entities = get_trip_entities(trip)

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

    return render_template("trip_details.html",
                            trip_id=trip_id,
                            trip_name=trip_name,
                            trip_entities=trip_entities,
                            range_of_dates=range_of_dates)


@app.route("/add_trip_details/<trip_id>")
def add_trip_details_form(trip_id):
    """
    Displays a form depending on the which trip confirmation they would like to
    add.(TERRRIBLE ENGLISH)
    """

    trip = Trip.query.filter(Trip.trip_id == trip_id).first()
    trip_name = trip.trip_name

    return render_template("trip_details_form.html",
                            trip_id=trip_id,
                            trip_name=trip_name)


@app.route("/my_trips/<trip_id>", methods=["POST"])
def add_form_trip_details(trip_id):
    """Adds the newly submitted confirmation trip details to the database."""

    form_type = request.form.get("ftype", None)

    create_item(form_type, request.form, trip_id)
    
    # router_map = {"event": Event,
    #               "flight": Flight,
    #               "hotel": Hotel,
    #               "car-rental": CarRental,
    #               "public-transportation": PublicTransportation,
    #               "meeting": Meeting}

    # if form_type in router_map:
    #     instance = router_map[form_type]()
  
    # for key in request.form:
    #     if request.form[key] != "":
    #         if key == "start-date":
    #             datetime = make_start_datetime_obj()
    #             instance.starts_at = datetime
    #         elif key == "start-time":
    #             continue
    #         elif key == "end-date":
    #             datetime = make_end_datetime_obj()
    #             instance.ends_at = datetime
    #         elif key == "end-time":
    #             continue
    #         else:
    #             print request.form[key]
    #             setattr(instance, key, request.form[key])


    # instance.trip_id = trip_id

    # db.session.add(instance)
    # db.session.commit()

    return redirect("/my_trips/" + trip_id)


@app.route("/incoming_xml", methods=["POST"])
def process_incoming_xml():
    """Parses email XML and adds the parsed email trip details to the database."""

    xml_string = request.data

    worldmate_xml_parser(xml_string)

    # if 
    # create_item(email_type, , trip_id)




if __name__ == "__main__":

    connect_to_db(app)

    app.run(debug=True, host='0.0.0.0')
