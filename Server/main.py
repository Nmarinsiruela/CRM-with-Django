#!/usr/bin/env python

import endpoints
import datetime
from time import sleep

from login import log_in

from protorpc import message_types
from protorpc import remote

from messages import LoginRequest, LoginResponse
from models import User, Customer


@endpoints.api(name='crmAM', version='v1',
               allowed_client_ids=[endpoints.API_EXPLORER_CLIENT_ID],
               scopes=[endpoints.EMAIL_SCOPE])
class MainPage(remote.Service):

    @endpoints.method(LoginRequest, LoginResponse, path='login',
                      http_method='POST', name='login')
    def login(self, request):
        """
        Validates the login and returns the valid Client's data.
        """
        #workday_query = Workday.query(Workday.employee.email == "hrm@edosoft.es").get()
        #if workday_query is None:
        #    util.create_mock_user()
        
        user = endpoints.get_current_user()
        return log_in(user, request.name, request.surname)


app = endpoints.api_server([MainPage], restricted=False)
