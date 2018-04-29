from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse

# TODO: Acabar Updates

class UserTestCase(TestCase):
    def setUp(self):
        user = User.objects.create_user(username="admin", first_name="Admin", last_name="Agile", is_staff=True)
        user.set_password("Pass4312")
        user.save()
        self.client = Client()
# [START Read Tests #3]
    def test_get_list(self):
        User.objects.create(username="nestor", password="Pass4312", first_name="Nestor", last_name="Marin", is_staff=False)
        # print (response.context["user"].is_authenticated)
        self.client.login(username="admin", password="Pass4312")
        response = self.client.get(reverse('users:index'), follow=True)
        last_url = response.request['PATH_INFO']
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['user_list']), 2)
        # The List is showed in reverse. So the last user created is the first one to show.
        self.assertEqual(response.context['user_list'][0].username, "nestor")
        self.assertEqual('/users/', last_url)

    def test_get_list_not_logged(self):
        response = self.client.get(reverse('users:index'), follow=True)
        last_url = response.request['PATH_INFO']
        self.assertEqual(response.status_code, 200)
        self.assertEqual('/accounts/login/', last_url)

    def test_get_list_logged_but_not_permission(self):
        user = User.objects.create_user(username="not_admin", first_name="Admin", last_name="Agile", is_staff=False)
        user.set_password("Pass4312")
        user.save()
        self.client.login(username="not_admin", password="Pass4312")
        response = self.client.get(reverse('users:index'), follow=True)
        last_url = response.request['PATH_INFO']
        self.assertEqual(response.status_code, 200)
        self.assertEqual('/accounts/login/', last_url)

# [END   Read Tests]

# [START Create Tests #3]
    def test_create_user(self):
        self.client.login(username="admin", password="Pass4312")
        response = self.client.post('/users/create', {'username': "new_user", 'password': "Pass4444", "is_staff": False, "first_name": "PruebaTest"}, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['user_list']), 2)

    def test_create_user_empty_or_wrong_data(self):
        '''
        If the user doesn't fill the required fields of the form and submit it anyway, the system will not move from the create page.
        '''
        self.client.login(username="admin", password="Pass4312")
        response = self.client.post('/users/create', {'username': "", 'password': "Pass4444", "is_staff": False, "first_name": "PruebaTest"}, follow=True)
        self.assertEqual(response.status_code, 200)
        last_url = response.request['PATH_INFO']
        self.assertEqual('/users/create', last_url)
        self.assertEqual(len(User.objects.all()), 1)

    def test_create_duplicate(self):
        self.client.login(username="admin", password="Pass4312")
        response = self.client.post('/users/create', {'username': "new_user", 'password': "Pass4444", "is_staff": False, "first_name": "PruebaTest"}, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['user_list']), 2)

        response = self.client.post('/users/create', {'username': "new_user", 'password': "Pass4444", "is_staff": False, "first_name": "PruebaTest"}, follow=True)
        self.assertEqual(response.status_code, 200)
        last_url = response.request['PATH_INFO']
        self.assertEqual('/users/create', last_url)
        self.assertEqual(len(User.objects.all()), 2)

# [END   Create Tests]

# [START Delete Tests]
    def test_delete_user(self):
        u = User.objects.create(username="nestor", password="Pass4312", first_name="Nestor", last_name="Marin", is_staff=False)
        self.client.login(username="admin", password="Pass4312")
        response = self.client.post('/users/{0}/delete'.format(u.id), follow=True)
        last_url = response.request['PATH_INFO']
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['user_list']), 1)
        self.assertEqual('/users/', last_url)

    def test_delete_own_user(self):
        self.client.login(username="admin", password="Pass4312")
        u = User.objects.get(username="admin")
        response = self.client.post('/users/{0}/delete'.format(u.id), follow=True)
        last_url = response.request['PATH_INFO']
        self.assertEqual(response.status_code, 200)
        self.assertEqual('/users/', last_url)

# [END   Delete Tests]

# [START Update Tests]

    def test_update(self):
        u = User.objects.create(username="nestor", password="Pass4312", first_name="Nestor", last_name="Marin", is_staff=False)
        self.client.login(username="admin", password="Pass4312")
        response = self.client.post('/users/{0}/update'.format(u.id), {"username": "nestor" ,"is_staff": False, "first_name": "PruebaUpd", "last_name": "PruebaUpd"}, follow=True)
        last_url = response.request['PATH_INFO']
        self.assertEqual(response.status_code, 200)
        self.assertEqual('/users/{0}/'.format(u.id), last_url)

    def test_update_invalid_user(self):
        self.client.login(username="admin", password="Pass4312")
        response = self.client.post('/users/{0}/update'.format("999"), {"is_staff": False, "first_name": "PruebaUpd", "last_name": "PruebaUpd"}, follow=True)
        self.assertEqual(response.status_code, 404)

    def test_update_invalid_data(self):
        u = User.objects.create(username="nestor", password="Pass4312", first_name="Nestor", last_name="Marin", is_staff=False)
        self.client.login(username="admin", password="Pass4312")
        response = self.client.post('/users/{0}/update'.format(u.id), {"username": "", "is_staff": False, "first_name": "PruebaUpd", "last_name": "PruebaUpd"}, follow=True)
        last_url = response.request['PATH_INFO']
        self.assertEqual(response.status_code, 200)
        self.assertEqual('/users/{0}/update'.format(u.id), last_url)       
    '''

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
    '''
# [END   Update Tests]

# [START Access Tests]
    def test_any_action_no_admin(self):
        """
        Any Admin-privileged action needs to be issued by an Admin. If the User who sents the request has no Admin attribute,
        it will be inmediately denied.
        """
        User.objects.create(username="noadmin", password="Pass4312", first_name="NoAdmin", last_name="Marin", is_staff=False)

        u = User.objects.create(username="nestor", password="Pass4312", first_name="Nestor", last_name="Marin", is_staff=False)

        self.client.login(username="noadmin", password="Pass4312")
        response = self.client.post('/users/{0}/delete'.format(u.id), follow=True)
        last_url = response.request['PATH_INFO']
        self.assertEqual(response.status_code, 200)
        self.assertEqual('/accounts/login/', last_url)

        response = self.client.get(reverse('users:index'), follow=True)
        last_url = response.request['PATH_INFO']
        self.assertEqual(response.status_code, 200)
        self.assertEqual('/accounts/login/', last_url)

        response = self.client.post('/users/create', {'username': "new_user", 'password': "Pass4444", "is_staff": False, "first_name": "PruebaTest"}, follow=True)
        last_url = response.request['PATH_INFO']
        self.assertEqual(response.status_code, 200)
        self.assertEqual('/accounts/login/', last_url)

        response = self.client.post('/users/{0}/update'.format(u.id), {'username': "user_updated", 'password': "Pass4444", "is_staff": False, "first_name": "PruebaUpd"}, follow=True)
        last_url = response.request['PATH_INFO']
        self.assertEqual(response.status_code, 200)
        self.assertEqual('/accounts/login/', last_url)

    def test_any_action_no_logged(self):
        """
        Any Admin-privileged action needs to be issued by an Admin. If the User is not logged in,
        it will be inmediately denied, regardless if the User is a valid admin.
        """
        u = User.objects.create(username="nestor", password="Pass4312", first_name="Nestor", last_name="Marin", is_staff=False)

        response = self.client.post('/users/{0}/delete'.format(u.id), follow=True)
        last_url = response.request['PATH_INFO']
        self.assertEqual(response.status_code, 200)
        self.assertEqual('/accounts/login/', last_url)

        response = self.client.get(reverse('users:index'), follow=True)
        last_url = response.request['PATH_INFO']
        self.assertEqual(response.status_code, 200)
        self.assertEqual('/accounts/login/', last_url)

        response = self.client.post('/users/create', {'username': "new_user", 'password': "Pass4444", "is_staff": False, "first_name": "PruebaTest"}, follow=True)
        last_url = response.request['PATH_INFO']
        self.assertEqual(response.status_code, 200)
        self.assertEqual('/accounts/login/', last_url)

        response = self.client.post('/users/{0}/update'.format(u.id), {'username': "user_updated", 'password': "Pass4444", "is_staff": False, "first_name": "PruebaUpd"}, follow=True)
        last_url = response.request['PATH_INFO']
        self.assertEqual(response.status_code, 200)
        self.assertEqual('/accounts/login/', last_url)

# [END   Access Tests]
    
    