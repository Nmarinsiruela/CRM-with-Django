from rest_framework.test import APITestCase, APIClient
from .models import Customer
from django.contrib.auth.models import User
from django.urls import reverse


class UserTestCase(APITestCase):
    def setUp(self):
        '''
        Two users are created and stored into the test database.
        '''
        user = User.objects.create_user(username='admin', first_name='Admin', last_name='Agile', is_staff=True)
        user.set_password('Pass4312')
        user.save()

        user = User.objects.create_user(username='creator', first_name='Customer', last_name='Testing', is_staff=False)
        user.set_password('Pass4312')
        user.save()

        self.user_creator = user
        self.client = APIClient()


# [START Access Tests]
    def test_any_action_no_logged(self):
        '''
        Any Customer-related action needs to be issued by a logged User. If the User is not logged in,
        it will be inmediately denied.
        '''
        User.objects.get(id=1)
        cu = Customer.objects.create(name='Nestor', surname='Marin', created_by_user=self.user_creator)

        response = self.client.delete('/customers/{0}/'.format(cu.id))
        self.assertEqual(response.status_code, 403)

        response = self.client.get('/customers/')
        self.assertEqual(response.status_code, 403)

        response = self.client.post('/customers/create', {'name': 'Test', 'surname': 'Agile'})
        self.assertEqual(response.status_code, 403)

        response = self.client.put('/customers/{0}/'.format(cu.id), {'name': 'Customer', 'surname': 'Updated'})
        self.assertEqual(response.status_code, 403)
        
# [END   Access Tests]

# [START Create Tests #3]

    '''
    Special considerations:
    Create provides the following properties to be typed in its form: 
        *name.
        *surname.
        photo.
    '''
    def test_create_customer(self):
        self.client.login(username='creator', password='Pass4312')
        response = self.client.post('/customers/create', {'name': 'new_user', 'surname': 'customer', 'created_by_user': self.user_creator.username})
        self.assertEqual(response.status_code, 201)
        self.assertEqual(len(Customer.objects.all()), 1)

        response = self.client.get('/customers/1/')
        self.assertEqual(response.data['created_by_user'], self.user_creator.username)

    def test_create_customer_empty_or_wrong_data(self):
        self.client.login(username='creator', password='Pass4312')
        response = self.client.post('/customers/create', {'name': '', 'surname': ''})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(len(Customer.objects.all()), 0)
# [END   Create Tests]

# [START Read Tests #3]
    def test_get_list(self):
        self.client.login(username='admin', password='Pass4312')
        c = Customer(name='Test', surname='Agile', created_by_user=self.user_creator)
        c.save()
        c = Customer(name='Test', surname='Agile', created_by_user=self.user_creator)
        c.save()
        c = Customer(name='Test', surname='Agile', created_by_user=self.user_creator)
        c.save()
        response = self.client.get('/customers/')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 3)

# [END   Read Tests]

# [START Delete Tests]
    def test_delete_customer(self):
        self.client.login(username='admin', password='Pass4312')
        c = Customer(name='Test', surname='Agile', created_by_user=self.user_creator)
        c.save()
        response = self.client.delete('/customers/{0}/'.format(c.id))

        self.assertEqual(response.status_code, 204)

        response = self.client.get('/customers/')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 0)

# [END   Delete Tests]

# [START Update Tests]

    def test_update(self):
        self.client.login(username='admin', password='Pass4312')
        u = User.objects.get(username='admin')
        c = Customer(name='Test', surname='Agile', created_by_user=self.user_creator.username)
        c.save()
        response = self.client.put('/customers/{0}/'.format(c.id), {'name': 'Agile' ,'surname': 'Test'})
        self.assertEqual(response.status_code, 200)

        self.assertEqual(response.data['created_by_user'], self.user_creator.username)
        self.assertEqual(response.data['last_modified_by_user'], u.username)

    def test_update_invalid_data(self):
        self.client.login(username='admin', password='Pass4312')
        u = User.objects.get(username='admin')
        c = Customer(name='Test', surname='Agile', created_by_user=self.user_creator)
        c.save()

        response = self.client.put('/customers/{0}/'.format(c.id), {'name': '' ,'surname': 'Test'})
        self.assertEqual(response.status_code, 400)
    
    def test_update_invalid_customer(self):
        self.client.login(username='admin', password='Pass4312')
        response = self.client.put('/customers/{0}/'.format('999'), {'name': 'Agile' ,'surname': 'Test'})
        self.assertEqual(response.status_code, 404)

# [END   Update Tests]


# [START Access Tests]
    def test_any_action_no_admin(self):
        '''
        Any Admin-privileged action needs to be issued by an Admin. If the User who sents the request has no Admin attribute,
        it will be inmediately denied.
        '''
        User.objects.create(username='noadmin', password='Pass4312', first_name='NoAdmin', last_name='Marin', is_staff=False)

        u = User.objects.create(username='nestor', password='Pass4312', first_name='Nestor', last_name='Marin', is_staff=False)

        self.client.login(username='noadmin', password='Pass4312')
        response = self.client.delete('/users/{0}/'.format(u.id))
        
        self.assertEqual(response.status_code, 403)

        response = self.client.get('/users/')
        self.assertEqual(response.status_code, 403)
        
        response = self.client.post('/users/create', {'username': 'new_user', 'password': 'Pass4444', 'is_staff': False, 'first_name': 'PruebaTest'})
        self.assertEqual(response.status_code, 403)
        
        response = self.client.put('/users/{0}/'.format(u.id), {'username': 'user_updated', 'password': 'Pass4444', 'is_staff': False, 'first_name': 'PruebaUpd'})
        self.assertEqual(response.status_code, 403)
        

    def test_any_admin_action_no_logged(self):
        '''
        Any Admin-privileged action needs to be issued by an Admin. If the User is not logged in,
        it will be inmediately denied.
        '''
        u = User.objects.create(username='nestor', password='Pass4312', first_name='Nestor', last_name='Marin', is_staff=False)

        response = self.client.delete('/users/{0}/'.format(u.id))
        self.assertEqual(response.status_code, 403)

        response = self.client.get('/users/')
        self.assertEqual(response.status_code, 403)
        
        response = self.client.post('/users/create', {'username': 'new_user', 'password': 'Pass4444', 'is_staff': False, 'first_name': 'PruebaTest'})
        self.assertEqual(response.status_code, 403)
        
        response = self.client.put('/users/{0}/'.format(u.id), {'username': 'user_updated', 'password': 'Pass4444', 'is_staff': False, 'first_name': 'PruebaUpd'})
        self.assertEqual(response.status_code, 403)
        

# [END   Access Tests]


# [START Create Tests #3]
    '''
    Special considerations:
    Create provides the following properties to be typed in its form: 
        *username - Must be unique to the whole database.
        *password
        first_name
        last_name
        is_staff.
    An User cannot change its own Admin privilege.
    '''
    def test_create_user(self):
        self.client.login(username='admin', password='Pass4312')
        response = self.client.post('/users/create', {'username': 'new_user', 'password': 'Pass4444', 'is_staff': False, 'first_name': 'PruebaTest'})
        self.assertEqual(response.status_code, 201)

        response = self.client.get('/users/')
        self.assertEqual(len(response.data), 3)

    def test_create_user_empty_or_wrong_data(self):
        self.client.login(username='admin', password='Pass4312')
        response = self.client.post('/users/create', {'username': '', 'password': 'Pass4444', 'is_staff': False, 'first_name': 'PruebaTest'})
        self.assertEqual(response.status_code, 400)
        
        response = self.client.get('/users/')
        self.assertEqual(len(response.data), 2)

    def test_create_duplicate(self):
        self.client.login(username='admin', password='Pass4312')
        response = self.client.post('/users/create', {'username': 'new_user', 'password': 'Pass4444', 'is_staff': False, 'first_name': 'PruebaTest'})
        self.assertEqual(response.status_code, 201)
        
        response = self.client.post('/users/create', {'username': 'new_user', 'password': 'Pass4444', 'is_staff': False, 'first_name': 'PruebaTest'})
        self.assertEqual(response.status_code, 400)
        
        response = self.client.get('/users/')
        self.assertEqual(len(response.data), 3)

# [END   Create Tests]


# [START Read Tests #3]
    def test_get_userlist(self):
        User.objects.create(username='nestor', password='Pass4312', first_name='Nestor', last_name='Marin', is_staff=False)

        self.client.login(username='admin', password='Pass4312')
        response = self.client.get('/users/')
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 3)

# [END   Read Tests]


# [START Delete Tests]
    '''
    Special considerations:
    Delete doesn't enable the User to delete its own account.
    '''
    def test_delete_user(self):
        u = User.objects.create(username='nestor', password='Pass4312', first_name='Nestor', last_name='Marin', is_staff=False)
        self.client.login(username='admin', password='Pass4312')
        response = self.client.delete('/users/{0}/'.format(u.id))
        self.assertEqual(response.status_code, 204)

    def test_delete_own_user(self):
        self.client.login(username='admin', password='Pass4312')
        u = User.objects.get(username='admin')
        response = self.client.delete('/users/{0}/'.format(u.id))
        self.assertEqual(response.status_code, 406)
        

# [END   Delete Tests]

# [START Update Tests]
    '''
    Special considerations:
    Update doesn't enable the User to change the password of an account, only provide changes to: 
        username
        first_name
        last_name
        is_staff.
    An User cannot change its own Admin privilege.
    '''
    def test_update_user(self):
        u = User.objects.create(username='nestor', password='Pass4312', first_name='Nestor', last_name='Marin', is_staff=False)
        self.client.login(username='admin', password='Pass4312')
        response = self.client.put('/users/{0}/'.format(u.id), {'username': 'nestor' ,'is_staff': False, 'first_name': 'PruebaUpd', 'last_name': 'PruebaUpd'})
        self.assertEqual(response.status_code, 200)

    def test_update_invalid_user(self):
        self.client.login(username='admin', password='Pass4312')
        response = self.client.put('/users/{0}/'.format('999'), {'is_staff': False, 'first_name': 'PruebaUpd', 'last_name': 'PruebaUpd'})
        self.assertEqual(response.status_code, 404)

    def test_update_invalid_data_user(self):
        u = User.objects.create(username='nestor', password='Pass4312', first_name='Nestor', last_name='Marin', is_staff=False)
        self.client.login(username='admin', password='Pass4312')
        response = self.client.put('/users/{0}/'.format(u.id), {'username': '', 'is_staff': False, 'first_name': 'PruebaUpd', 'last_name': 'PruebaUpd'})
        
        self.assertEqual(response.status_code, 400)

    def test_update_own_user_no_admin_change(self):
        u = User.objects.get(username='admin')
        self.client.login(username='admin', password='Pass4312')
        response = self.client.put('/users/{0}/'.format(u.id), {'username': 'admin' ,'is_staff': True, 'first_name': 'PruebaUpd', 'last_name': 'PruebaUpd'})
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(u.is_staff, True)

    def test_update_own_user_admin_change(self):
        u = User.objects.get(username='admin')
        self.client.login(username='admin', password='Pass4312')
        response = self.client.put('/users/{0}/'.format(u.id), {'username': 'admin' ,'is_staff': False, 'first_name': 'PruebaUpd', 'last_name': 'PruebaUpd'})
        
        self.assertEqual(response.status_code, 406)
        self.assertEqual(u.is_staff, True)
# [END   Update Tests]