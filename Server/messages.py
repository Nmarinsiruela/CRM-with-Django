#!/usr/bin/env python

from protorpc import messages
from protorpc import message_types

# TODO: Create the Customer Messages

# [LOGIN MESSAGES - START]
class LoginRequest(messages.Message):
    """
    The request will be done by GSuite. No more information is needed than the name and surname, 
    as if it's a new user its is_admin field will be created automatically.
    """
    name = messages.StringField(1)
    surname = messages.StringField(2)

class LoginResponse(messages.Message):
    """
    The server response to a correct login request will return the full data of the User, along with a response_code of 200.
    """
    response_code = messages.IntegerField(1, required=True)
    text = messages.StringField(2, required=True)
    name = messages.StringField(3)
    surname = messages.StringField(4)
    is_admin = messages.BooleanField(5)

# [LOGIN MESSAGES - END]

# [ADMIN MESSAGES - START]
class AdminCreateRequest(messages.Message):
    """
    A correct create_user request will require all the necessary fields that compose an User model.
    """
    email = messages.StringField(1, required=True)
    name = messages.StringField(2, required=True)
    surname = messages.StringField(3, required=True)
    is_admin = messages.BooleanField(4, required=True)

class AdminDeleteRequest(messages.Message):
    """
    As an User is easily identified by its email field, that's the only element requested for a delete.
    """
    email = messages.StringField(1, required=True)

class AdminUpdateRequest(messages.Message):
    """
    Updating the data of an user requires its email for an identification, but the rest of its fields can be updated or not, depending on
    the provided data.
    """
    selected_email = messages.StringField(1, required=True)
    email = messages.StringField(2)
    name = messages.StringField(3)
    surname = messages.StringField(4)
    is_admin = messages.BooleanField(5)

class AdminResponse(messages.Message):
    """
    Any type of response of the system would not need to return an object, but instead a correct response_code.
    """
    response_code = messages.IntegerField(1, required=True)
    text = messages.StringField(2, required=True)

class AdminGetListUsersResponse(messages.Message):
    """
    When an Admin asks for the whole list of users, it'll receive an array of AdminCreateRequest elements, which have all
    the fields that comprise an User model.
    """
    response_code = messages.IntegerField(1, required=True)
    text = messages.StringField(2, required=True)
    users = messages.MessageField(AdminCreateRequest, 3, repeated=True)

# [ADMIN MESSAGES - END]