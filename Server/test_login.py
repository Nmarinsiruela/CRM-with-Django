from google.appengine.ext import ndb
from google.appengine.ext import testbed

import unittest

from messages import LoginRequest, LoginResponse
from models import User
from login import log_in
# [END imports]

# [START datastore_example_test]
class DatastoreTestCase(unittest.TestCase):

    def setUp(self):
        # First, create an instance of the Testbed class.
        self.testbed = testbed.Testbed()
        # Then activate the testbed, which prepares the service stubs for use.
        self.testbed.activate()
        # Next, declare which service stubs you want to use.
        self.testbed.init_datastore_v3_stub()
        self.testbed.init_memcache_stub()
        # Clear ndb's in-context cache between tests.
        # This prevents data from leaking between tests.
        # Alternatively, you could disable caching by
        # using ndb.get_context().set_cache_policy(False)
        ndb.get_context().clear_cache()
        self.user = User(email="test@agilemonkeys.com", name="Test", surname="Agile", is_admin=True)

# [START User Tests]
    def test_new_valid_user(self):
        result = log_in(self.user, self.user.name, self.user.surname, True)
        self.assertEqual(result.text, "New User Created")

    def test_returning_user(self):
        self.user.put()
        result = log_in(self.user, self.user.name, self.user.surname, True)
        self.assertEqual(result.text, "Correct Login")
        self.assertEqual(result.is_admin, True)

    def test_returning_user_2(self):
        valid_user = User(email="nmarinsiruela@gmail.com", name="Nestor", surname="Marin", is_admin=False)
        valid_user.put()
        result = log_in(valid_user, valid_user.name, valid_user.surname, True)
        self.assertEqual(result.text, "Correct Login")
        self.assertEqual(result.is_admin, False)

    def test_no_user(self):
        result = log_in(None, None, None, True)
        self.assertEqual(result.text, "Error. Invalid Data")

    def test_invalid_user(self):
        invalid_user = User(email="test@test.com", name="Bad", surname="Test", is_admin=True)
        result = log_in(invalid_user, invalid_user.name, invalid_user.surname, True)
        self.assertEqual(result.text, "Error. Invalid User Domain")
# [END   User Tests]


# [START main]
if __name__ == '__main__':
    unittest.main()
# [END main]
