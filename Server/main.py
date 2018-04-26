#!/usr/bin/env python

import endpoints
import datetime
from time import sleep

from login import log_in
from admin import create_user, delete_user, update_user, get_all_users
from protorpc import message_types
from protorpc import remote

from messages import LoginRequest, LoginResponse
from messages import AdminCreateRequest, AdminDeleteRequest, AdminGetListUsersResponse, AdminUpdateRequest, AdminResponse
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
        
        user = endpoints.get_current_user()
        return log_in(user, request.name, request.surname)

    @endpoints.method(AdminCreateRequest, AdminResponse, path='create',
                      http_method='POST', name='create')
    def create(self, request):
        """
        Creates a new User entity with the provided data.
        """
        
        user = endpoints.get_current_user()
        return create_user(user, request.email, request.name, request.surname, request.is_admin)

    @endpoints.method(AdminDeleteRequest, AdminResponse, path='create',
                      http_method='POST', name='create')
    def delete(self, request):
        """
        Deletes the selected User entity.
        """
        
        user = endpoints.get_current_user()
        return delete_user(user, request.email)

    @endpoints.method(AdminUpdateRequest, AdminResponse, path='update',
                      http_method='POST', name='update')
    def update(self, request):
        """
        Updates the selected User entity.
        """
        user = endpoints.get_current_user()
        return update_user(user, request.selected_email, request.email, request.name, request.surname, request.is_admin)

    @endpoints.method(message_types.VoidMessage, AdminGetListUsersResponse, path='get_list',
                      http_method='POST', name='get_list')
    def get_list(self, request):
        """
        Get the list of all the User entities.
        """
        user = endpoints.get_current_user()
        return delete_user(user, request.email)

app = endpoints.api_server([MainPage], restricted=False)
