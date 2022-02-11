"""User model tests."""

# run these tests like:
#
#    python -m unittest test_user_model.py


import os
from unittest import TestCase
from flask import session

from models import db, User, Message, Follows

# BEFORE we import our app, let's set an environmental variable
# to use a different database for tests (we need to do this
# before we import our app, since that will have already
# connected to the database

os.environ['DATABASE_URL'] = "postgresql:///warbler_test"

# Now we can import app

from app import app, CURR_USER_KEY

# Create our tables (we do this here, so we only create the tables
# once for all tests --- in each test, we'll delete the data
# and create fresh new clean test data

db.create_all()

app.config['WTF_CSRF_ENABLED'] = False


class UserModelTestCase(TestCase):
    """Test views for messages."""

    def setUp(self):
        """Create test client, add sample data."""

        User.query.delete()
        Message.query.delete()
        Follows.query.delete()

        self.client = app.test_client()

        self.u = User(
        email="test@test.com",
        username="testuser",
        password="HASHED_PASSWORD"
        )

        self.u2 = User(
        email="test2@test.com",
        username="testuser2",
        password="HASHED_PASSWORD"
        )

        db.session.add_all([self.u, self.u2])
        db.session.commit()


    def test_user_model(self):
        """Does basic model work?"""

        # User should have no messages & no followers
        self.assertEqual(len(self.u.messages), 0)
        self.assertEqual(len(self.u.followers), 0)
        
        self.assertEqual(self.u.image_url, "/static/images/default-pic.png")

        self.assertEqual(str(self.u), f"<User #{self.u.id}: testuser, test@test.com>")

    def test_is_followed_by(self):
        """Is u followed by u2?
        Is u2 not following u?"""

        self.u.followers.append(self.u2)

        self.assertEqual(self.u.is_followed_by(self.u2), True)


    # def test_is_following(self):
    #     """Is u2 following u?"""

    #     self.u2.following.append(self.u)

    #     self.assertEqual(self.u2.following, [self.u])

            # with self.client as c:
        #     with c.session_transaction() as sess:
        #         sess[CURR_USER_KEY] = self.u.id
        #     resp = c.post(f"/users/follow/{self.u.id}")

        #     self.assertEqual(resp.status_code, 302)
        #     self.assertEqual(len(self.u.followers), 1)

