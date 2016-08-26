import unittest
from server import app
from model import db, connect_to_db


class FlaskTests(unittest.TestCase):
    """Integration Tests: Tests flasks server."""

    def setUp(self):
        """Stuff to do before every test."""

        self.client = app.test_client()
        app.config['TESTING'] = True

    def test_homepage(self):
        """Tests homepage."""

        result = self.clinet.get("/")
        self.assertEqual(result.status_code, 200)
        self.assertIn("Login, Sign Up, Welcome", result.data)
        print "Completed homepage test"


class DatabaseTests(unittest.TestCase):
    """Integration Tests: Tests data that uses the database."""

    def setUp(self):
        """Stuff to do before every test."""

        app.config["TESTING"] = True
        app.config["SECRET_KEY"] = "ABC"
        self.client = app.test_client()
        connect_to_db(app, "postgresql:///testdb")

    def tearDown(self):
        db.session.close()

    def test_signup_submit(self):
        """Tests user sign up."""

        result = self.client.post("/signup",
                                   data={"firstname": "Lauren", "lastname": "Budd",
                                   "email": "laurenb@gmail.com", "password": "test123"},
                                   follow_redirects=True)
        self.assertIn("Login, Sign Up, Welcome", result.data)

    def test_login_submit(self):
        """Tests user login."""

        result = self.client.post("/login",
                                   data={"email": "laurenb@gmail.com", "password": "test123"},
                                   follow_redirects=True)
        self.asserIn("Add an Event, Return to My Trips, Rome", result.data)

    def logout(self):
        """Tests logout route."""

    def test_all_trips(self):
        """"Tests a users my trip page."""

        with self.client as c:
            with c.session_transaction() as sess:
                sess["user_id"] = 1
            self.assertIn("Create new trip, Rome, Wed", result.data)

    def add_new_trip(self):
        result = self.client.post("/my_trips",
                                   data={"trip_name": "Rome", "destination": "Rome", 
                                   "start_date": "2016-08-10 00:00:00", "end_date": "2016-09-20 00:00:00"},
                                   follow_redirects=True)
        self.asserIn("Create new trip, My Trips, Rome", result.data)

    def test_trip_details(self):
        """Tests a users trip detail page."""

        result = self.client.get("/my_trips/1")
        self.assertIn("Depart, Duration, Show more details", result.data)

    def test_add_form_trip_details(self):
        result = self.client.post("/my_trips/<trip_id>",
                                   data={"meeting_subject": "Uber", "address": "123 Cooper St, Oakland, CA",
                                   "starts_at": "2016-08-26 18:00:00"},
                                   follow_redirects=True)
        self.asserIn("Add an Event, Return to My Trips, Uber", result.data)

