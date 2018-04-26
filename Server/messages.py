#!/usr/bin/env python

from protorpc import messages
from protorpc import message_types

class LoginRequest(messages.Message):
    name = messages.StringField(1)
    surname = messages.StringField(2)
    is_admin = messages.BooleanField(3)

class LoginResponse(messages.Message):
    response_code = messages.IntegerField(1, required=True)
    text = messages.StringField(2, required=True)
    name = messages.StringField(3)
    surname = messages.StringField(4)
    is_admin = messages.BooleanField(5)

class AdminCreateRequest(messages.Message):
    email = messages.StringField(1, required=True)
    name = messages.StringField(2, required=True)
    surname = messages.StringField(3, required=True)
    is_admin = messages.BooleanField(4, required=True)

class AdminDeleteRequest(messages.Message):
    email = messages.StringField(1, required=True)

class AdminUpdateRequest(messages.Message):
    email = messages.StringField(1, required=True)
    name = messages.StringField(2)
    surname = messages.StringField(3)
    is_admin = messages.BooleanField(4)

class AdminResponse(messages.Message):
    response_code = messages.IntegerField(1, required=True)
    text = messages.StringField(2, required=True)

class AdminGetListUsersResponse(messages.Message):
    response_code = messages.IntegerField(1, required=True)
    text = messages.StringField(2, required=True)
    users = messages.MessageField(AdminCreateRequest, 3, repeated=True)

