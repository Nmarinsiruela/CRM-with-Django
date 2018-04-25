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
        self.user = User(email="test@test.com", name="Test", surname="Agile", is_admin=True)

# [START User Tests]
    def test_no_user(self):
        result = log_in(self.user, self.user.name, self.user.surname, True)
        self.assertEqual(result.text, "New Login")

    def test_returning_user(self):
        self.user.put()
        result = log_in(self.user, self.user.name, self.user.surname, True)
        self.assertEqual(result.text, "Correct Login")
        self.assertEqual(result.is_admin, True)
# [END   User Tests]


# [START main]
if __name__ == '__main__':
    unittest.main()
# [END main]
