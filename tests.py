import unittest
from server import app
from model import example_data, connect_to_db, db


class FlaskTests(unittest.TestCase):
    """Integration Tests: Tests flasks server."""

    def setUp(self):
        """Stuff to do before every test."""

        self.client = app.test_client()
        app.config['TESTING'] = True

    def test_homepage(self):
        """Tests homepage."""

        result = self.client.get("/")
        self.assertEqual(result.status_code, 200)
        self.assertIn("Wanderlust", result.data)
        print "Completed homepage test"


class DatabaseTests(unittest.TestCase):
    """Integration Tests: Tests data that uses the database."""

    def setUp(self):
        """Stuff to do before every test."""

        app.config["TESTING"] = True
        app.config["SECRET_KEY"] = "ABC"
        self.client = app.test_client()
        connect_to_db(app, "postgresql:///testdb")
        db.create_all()
        example_data()

    def tearDown(self):
        db.session.close()
        db.drop_all()

    def test_signup_submit(self):
        """Tests user sign up."""

        result = self.client.post("/signup",
                                   data={"firstname": "Lauren", "lastname": "Budd",
                                   "email": "laurenb@gmail.com", "password": "123456"},
                                   follow_redirects=True)
        self.assertIn("Wanderlust", result.data)

    def test_login_submit(self):
        """Tests user login."""

        result = self.client.post("/login",
                                   data={"email": "laurenb@gmail.com", "password": "123456"},
                                   follow_redirects=True)
        self.assertIn("Create new trip", result.data)

    # def logout(self):
    #     """Tests logout route."""

    def test_all_trips(self):
        """"Tests a users my trip page."""

        with self.client as c:
            with c.session_transaction() as sess:
                sess["logged_in"] = "laurenb@gmail.com"
            result = c.get("/my_trips", follow_redirects=True)
            self.assertIn("Create new trip", result.data)

    def add_new_trip(self):
        """Tests that a trip is added correctly to database."""

        result = self.client.post("/my_trips",
                                   data={"trip_name": "Rome", "destination": "Rome",
                                   "start_date": "2016-08-10 00:00:00", "end_date":
                                   "2016-09-20 00:00:00"}, follow_redirects=True)
        self.assertIn("Create new trip", result.data)

    def test_trip_details(self):
        """Tests a users trip detail page."""

        result = self.client.get("/my_trips/1")
        self.assertIn("Show more details", result.data)

    def test_add_form_trip_details(self):
        """Tests that trip details from a form are added correctly to database."""

        result = self.client.post("/my_trips/1",
                                   data={"ftype": "meeting", "meeting_subject": "Uber", "address": "123 Cooper St, Oakland, CA",
                                   "starts_at": "2016-08-26 18:00:00"},
                                   follow_redirects=True)
        self.assertIn("Add an Event", result.data)



if __name__ == "__main__":
    unittest.main()
