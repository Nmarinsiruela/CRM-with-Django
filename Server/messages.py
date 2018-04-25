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


