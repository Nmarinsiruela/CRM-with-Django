from django.test import TestCase, Client
from .models import Customer
from django.contrib.auth.models import User
from django.urls import reverse


class UserTestCase(TestCase):
    def setUp(self):
        '''
        Two crm are created and stored into the test database.
        '''
        user = User.objects.create_user(username='admin', first_name='Admin', last_name='Agile', is_staff=False)
        user.set_password('Pass4312')
        user.save()

        user = User.objects.create_user(username='creator', first_name='Customer', last_name='Testing', is_staff=False)
        user.set_password('Pass4312')
        user.save()

        self.user_creator = user
        self.client = Client()


# [START Access Tests]
    def test_any_action_no_logged(self):
        '''
        Any Customer-related action needs to be issued by a logged User. If the User is not logged in,
        it will be inmediately denied.
        '''
        User.objects.get(id=1)
        cu = Customer.objects.create(name='Nestor', surname='Marin', referenced_user=self.user_creator)

        response = self.client.post('/crm/{0}/delete'.format(cu.id), follow=True)
        last_url = response.request['PATH_INFO']
        self.assertEqual(response.status_code, 200)
        self.assertEqual('/accounts/login/', last_url)

        response = self.client.get(reverse('crm:index'), follow=True)
        last_url = response.request['PATH_INFO']
        self.assertEqual(response.status_code, 200)
        self.assertEqual('/accounts/login/', last_url)

        response = self.client.post('/crm/create', {'name': 'Test', 'surname': 'Agile'}, follow=True)
        last_url = response.request['PATH_INFO']
        self.assertEqual(response.status_code, 200)
        self.assertEqual('/accounts/login/', last_url)

        response = self.client.post('/crm/{0}/update'.format(cu.id), {'name': 'Customer', 'surname': 'Updated'}, follow=True)
        last_url = response.request['PATH_INFO']
        self.assertEqual(response.status_code, 200)
        self.assertEqual('/accounts/login/', last_url)

# [END   Access Tests]


# [START Create Tests #3]
    # TODO: Test with Photo

    '''
    Special considerations:
    Create provides the following properties to be typed in its form: 
        *name.
        *surname.
        photo.
    '''
    def test_create_customer(self):
        self.client.login(username='creator', password='Pass4312')
        response = self.client.post('/crm/create', {'name': 'new_user', 'surname': 'customer', 'referenced_user': self.user_creator}, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['latest_customer_list']), 1)

    def test_create_customer_empty_or_wrong_data(self):
        self.client.login(username='creator', password='Pass4312')
        response = self.client.post('/crm/create', {'name': '', 'surname': ''}, follow=True)
        self.assertEqual(response.status_code, 200)
        last_url = response.request['PATH_INFO']
        self.assertEqual('/crm/create', last_url)
# [END   Create Tests]

# [START Read Tests #3]
    def test_get_list(self):
        self.client.login(username='admin', password='Pass4312')
        c = Customer(name='Test', surname='Agile', referenced_user=self.user_creator)
        c.save()
        c = Customer(name='Test', surname='Agile', referenced_user=self.user_creator)
        c.save()
        c = Customer(name='Test', surname='Agile', referenced_user=self.user_creator)
        c.save()
        response = self.client.get(reverse('crm:index'), follow=True)
        last_url = response.request['PATH_INFO']

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['latest_customer_list']), 3)

        # The List is showed in reverse. So the last user created is the first one to show.
        self.assertEqual('/crm/', last_url)

# [END   Read Tests]


# [START Delete Tests]
    def test_delete_customer(self):
        self.client.login(username='admin', password='Pass4312')
        c = Customer(name='Test', surname='Agile', referenced_user=self.user_creator)
        c.save()
        response = self.client.post('/crm/{0}/delete'.format(c.id), follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['latest_customer_list']), 0)

# [END   Delete Tests]

# [START Update Tests]
    # TODO Test with photo

    def test_update(self):
        self.client.login(username='admin', password='Pass4312')
        u = User.objects.get(username='admin')
        c = Customer(name='Test', surname='Agile', referenced_user=self.user_creator)
        c.save()
        response = self.client.post('/crm/{0}/update'.format(c.id), {'name': 'Agile' ,'surname': 'Test', 'referenced_user': u}, follow=True)
        last_url = response.request['PATH_INFO']
        self.assertEqual(response.status_code, 200)
        self.assertEqual('/crm/{0}/'.format(u.id), last_url)
        self.assertEqual(response.context['customer'].referenced_user, u)

    def test_update_invalid_data(self):
        self.client.login(username='admin', password='Pass4312')
        u = User.objects.get(username='admin')
        c = Customer(name='Test', surname='Agile', referenced_user=self.user_creator)
        c.save()

        response = self.client.post('/crm/{0}/update'.format(u.id), {'name': '' ,'surname': 'Test', 'referenced_user': u}, follow=True)
        last_url = response.request['PATH_INFO']
        self.assertEqual(response.status_code, 200)
        self.assertEqual('/crm/{0}/update'.format(u.id), last_url)  
    
    def test_update_invalid_customer(self):
        self.client.login(username='admin', password='Pass4312')
        response = self.client.post('/crm/{0}/update'.format('999'), {'name': 'Agile' ,'surname': 'Test'}, follow=True)
        self.assertEqual(response.status_code, 404)

# [END   Update Tests]