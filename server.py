"""User Trips"""

from flask import Flask, render_template, redirect, request, flash, session

from model import User, Trip, Flight, Passenger, Hotel, CarRental
from model import PublicTransportation, Meeting, Event, connect_to_db, db
from model import make_start_datetime_obj, make_end_datetime_obj

import datetime

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

    if User.query.filter(User.email == email).first():
        flash("That email is already registered.  Please log in or choose a different email.")
        return redirect("/signup")
    else:
        new_user = User(email=email,
                        firstname=firstname,
                        lastname=lastname,
                        password=password)

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

    check_email = User.query.filter(User.email == email).first()

    if check_email:
        if check_email.password == password:
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
        user_id = current_user.user_id
    else:
        redirect("/login ")

    trips_list = []

    all_trips = Trip.query.filter(user_id == User.user_id).order_by(Trip.start_date).all()

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
    # trip_list = []

    # #not right, I need it to give me the different flights, hotels, etc.
    # current_trip = Trip.query.filter(Trip.trip_id == trip_id).first()

    # for item in current_trip:


    return render_template("trip_details.html",
                            trip_id=trip_id,
                            trip_name=trip_name)


@app.route("/add_trip_details/<trip_id>")
def add_trip_details_form(trip_id):
    """
    Displays a form depending on the which trip confirmation they would like to
    add.(TERRRIBLE ENGLISH)
    """

    return render_template("trip_details_form.html",
                            trip_id=trip_id)


@app.route("/my_trips/<trip_id>", methods=["POST"])
def add_trip_details(trip_id):
    """Adds the newly submitted confirmation trip details to the db and to the trip."""

    form_type = request.form.get("ftype", None)

    if form_type == "event":
        instance = Event()
        make_start_datetime_obj()
    elif form_type == "flight":
        instance = Flight()
        make_start_datetime_obj()
        make_end_datetime_obj()
    elif form_type == "hotel":
        instance = Hotel()
        make_start_datetime_obj()
        make_end_datetime_obj()
    elif form_type == "car-rental":
        instance = CarRental()
        make_start_datetime_obj()
        make_end_datetime_obj()
    elif form_type == "public-transportation":
        instance = PublicTransportation()
        make_start_datetime_obj()
        make_end_datetime_obj()
    elif form_type == "meeting":
        instance = Meeting()
        make_start_datetime_obj()
    
    for key in request.form:
        instance.key = request.form[key]


    return redirect("/my_trips/" + trip_id)


if __name__ == "__main__":

    connect_to_db(app)

    app.run(debug=True, host='0.0.0.0')
