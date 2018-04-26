from google.appengine.ext import ndb
from google.appengine.ext import testbed
import unittest

from messages import AdminResponse, AdminGetListUsersResponse
from models import User
from admin import create_user, delete_user, update_user, get_all_users
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
        self.admin = User(email="test@agilemonkeys.com", name="Test", surname="Agile", is_admin=True)

# [START Create Tests]
    
    def test_create_user(self):
        self.admin.put()
        valid_user = User(email='nmarinsiruela@gmail.com', name="Nestor", surname="Marin", is_admin=False)
        result = create_user(self.admin, valid_user.email, valid_user.name, valid_user.surname, valid_user.is_admin, True)
        self.assertEqual(result.text, "User Created")
        self.assertEqual(len(User.query().fetch()), 2)

    def test_create_user_empty_data(self):
        self.admin.put()
        valid_user = User(email="test@gmail.com", name="", surname="", is_admin=True)
        result = create_user(self.admin, valid_user.email, valid_user.name, valid_user.surname, valid_user.is_admin, True)
        self.assertEqual(result.response_code, 400)
        self.assertEqual(result.text, "All fields are mandatory")

    def test_create_user_invalid_data(self):
        self.admin.put()
        valid_user = User(email="test", name="", surname="", is_admin=True)
        result = create_user(self.admin, valid_user.email, valid_user.name, valid_user.surname, valid_user.is_admin, True)
        self.assertEqual(result.response_code, 400)
        self.assertEqual(result.text, "Invalid data found")

    def test_create_user_duplicate(self):
        self.admin.put()
        valid_user = User(email="nmarinsiruela@gmail.com", name="Nestor", surname="Marin", is_admin=False)
        create_user(self.admin, valid_user.email, valid_user.name, valid_user.surname, valid_user.is_admin, True)
        result = create_user(self.admin, valid_user.email, valid_user.name, valid_user.surname, valid_user.is_admin, True)
        self.assertEqual(result.text, "User is already Created")
        self.assertEqual(len(User.query().fetch()), 2)
    
# [END   Create Tests]

# [START Delete Tests]
    
    def test_delete_user(self):
        self.admin.put()

        valid_user = User(email="nmarinsiruela@gmail.com", name="Nestor", surname="Marin", is_admin=False)
        create_user(self.admin, valid_user.email, valid_user.name, valid_user.surname, valid_user.is_admin, True)
        self.assertEqual(2, len(User.query().fetch()))

        result = delete_user(self.admin, "nmarinsiruela@gmail.com", True)
        self.assertEqual(result.text, "User Deleted")
        self.assertEqual(1, len(User.query().fetch()))

    def test_delete_no_user(self):
        self.admin.put()
        result = delete_user(self.admin, "nmarinsiruela@gmail.com", True)
        self.assertEqual(result.text, "User not found")
        self.assertEqual(result.response_code, 400)
        self.assertEqual(1, len(User.query().fetch()))

    def test_delete_own_user(self):
        self.admin.put()
        result = delete_user(self.admin, self.admin.email, True)
        self.assertEqual(result.text, "You cannot delete yourself")
        self.assertEqual(result.response_code, 400)
    
# [END   Delete Tests]

# [START Update Tests]
    
    def test_update_user(self):
        self.admin.put()
        valid_user = User(email="nmarinsiruela@gmail.com", name="Nestor", surname="Marin", is_admin=False)
        create_user(self.admin, valid_user.email, valid_user.name, valid_user.surname, valid_user.is_admin, True)
        result = update_user(self.admin, valid_user.email, "newmail@gmail.com","Test", "Agile", True, True)
        self.assertEqual(2, len(User.query().fetch()))
        self.assertEqual(result.text, "User Updated")
        
        changed_used = User.query(User.email == "newmail@gmail.com").get()
        self.assertEqual(changed_used.name, "Test")

    def test_update_invalid_user(self):
        self.admin.put()
        result = update_user(self.admin, "user@user.com", "bad@gmail.com", None, None, None, True)
        self.assertEqual(result.text, "User not found")
        self.assertEqual(result.response_code, 400)

    def test_update_invalid_data(self):
        """
        If the user sends invalid data, the system won't change the stored elements.
        """
        self.admin.put()
        valid_user = User(email="nmarinsiruela@gmail.com", name="Nestor", surname="Marin", is_admin=False)
        create_user(self.admin, valid_user.email, valid_user.name, valid_user.surname, valid_user.is_admin, True)
        result = update_user(self.admin, valid_user.email, "nmarinsiruela", "", "Agile", None, True)
        self.assertEqual(result.text, "User Updated")
        self.assertEqual(result.response_code, 200)
        changed_used = User.query(User.email == "nmarinsiruela@gmail.com").get()
        self.assertEqual(changed_used.name, valid_user.name)
        self.assertEqual(changed_used.surname, "Agile")
        
    def test_update_own_user_no_admin_change(self):
        self.admin.put()
        result = update_user(self.admin, self.admin.email, self.admin.email, "NewName", "NewSurname", True, True)
        self.assertEqual(result.text, "User Updated")
        self.assertEqual(result.response_code, 200)

    def test_update_own_user_admin_change(self):
        self.admin.put()
        result = update_user(self.admin, self.admin.email,self.admin.email, "NewName", "NewSurname", False, True)
        self.assertEqual(result.text, "You cannot remove your admin privileges")
        self.assertEqual(result.response_code, 400)

    def test_update_own_user_email_change(self):
        self.admin.put()
        result = update_user(self.admin, self.admin.email, "newmail@new.com", "NewName", "NewSurname", True, True)
        self.assertEqual(result.text, "You cannot change your admin email")
        self.assertEqual(result.response_code, 400)
    
# [END   Update Tests]

# [START Read Tests]

    def test_get_list(self):
        self.admin.put()
        valid_user = User(email="nmarinsiruela@gmail.com", name="Nestor", surname="Marin", is_admin=False)
        create_user(self.admin, valid_user.email, valid_user.name, valid_user.surname, valid_user.is_admin, True)
        create_user(self.admin, "test@agile.com", "Name", "Surname", False, True)

        result = get_all_users(self.admin, True)
        self.assertEqual(len(result.users), 3)
        self.assertEqual(result.users[2].name, "Name")
        self.assertEqual(result.users[0].is_admin, True)

    def test_get_empty_list(self):
        self.admin.put()
        result = get_all_users(self.admin, True)
        self.assertEqual(len(result.users), 1)

# [END   Read Tests]

    def test_any_action_no_admin(self):
        """
        Any Admin-privileged action needs to be issued by an Admin. If the User who sents the request has no Admin attribute,
        it will be inmediately denied.
        """
        
        valid_user = User(email="nmarinsiruela@gmail.com", name="Nestor", surname="Marin", is_admin=False)
        result_create = create_user(valid_user, valid_user.email, valid_user.name, valid_user.surname, valid_user.is_admin, True)
        self.assertEqual(result_create.response_code, 400)
        self.assertEqual(result_create.text, "You don't have authorization to do this action")

        result_delete = delete_user(valid_user, valid_user.email, True)
        self.assertEqual(result_delete.response_code, 400)
        self.assertEqual(result_delete.text, "You don't have authorization to do this action")

        result_update = update_user(valid_user, valid_user.email, valid_user.email, valid_user.name, valid_user.surname, valid_user.is_admin, True)
        self.assertEqual(result_update.response_code, 400)
        self.assertEqual(result_update.text, "You don't have authorization to do this action")

        result_list = get_all_users(valid_user, True)
        self.assertEqual(result_list.response_code, 400)
        self.assertEqual(result_list.text, "You don't have authorization to do this action")


# [START main]
if __name__ == '__main__':
    unittest.main()
# [END main]
