from google.appengine.ext import ndb

# TODO: Insert User into Workday.


# [START Models]
class User(ndb.Model):
    """ Model of the User of the CRM. It has a special field, is_admin, which identifies an User with admin privileges."""
    email = ndb.StringProperty(indexed=True)
    name = ndb.StringProperty()
    surname = ndb.StringProperty()
    is_admin = ndb.BooleanProperty()

class Customer(ndb.Model):
    """ Model of the Customer of the CRM. """
    id = ndb.IntegerProperty(indexed=True)
    name = ndb.StringProperty()
    surname = ndb.StringProperty()
    # photo = ndb.BlobProperty()
# [END Models]
