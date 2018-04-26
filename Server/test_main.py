#!/usr/bin/env python

# Call in UNIX: python runner.py ~/google/google-cloud-sdk/platform/google_appengine
# Call in Bash: ~/AppData/Local/Google/Cloud\ SDK/google-cloud-sdk/platform/google_appengine/runner.py .
# Call in Windows (the file runner.py has to be in said path): "%HOME%\AppData\Local\Google\Cloud SDK\google-cloud-sdk\platform\google_appengine\runner.py" .


# Copyright 2016 Google Inc. All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# [START imports]
from google.appengine.ext import ndb
from google.appengine.ext import testbed

import unittest

from models import User
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

# [END datastore_example_test]

    # [START datastore_example_teardown]
    def tearDown(self):
        self.testbed.deactivate()
    # [END datastore_example_teardown]

    # [START datastore_example_insert]
    def testInsertEntity(self):
        User().put()
        self.assertEqual(1, len(User.query().fetch(2)))

    def testEntityOk(self):
        test = User(email="user@test.com")
        test.put()
        self.assertEqual("user@test.com", User.query().get().email)
    # [END datastore_example_insert]


# [START main]
if __name__ == '__main__':
    unittest.main()
# [END main]
