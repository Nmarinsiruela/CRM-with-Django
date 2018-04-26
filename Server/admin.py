import re

from messages import AdminResponse, AdminGetListUsersResponse, AdminCreateRequest
from models import User

def create_user(author, email, name, surname, is_admin, test=None):
    """
    Creates an user with the provided data from the Client. 
    The system will verify that the user is a valid Admin beforehand.
    The system will also verify that the provided data is correct.
    """

    admin_email = author.email() if test is None else author.email
    if verify_admin_status(admin_email) is False:
        return AdminResponse(text="You don't have authorization to do this action", response_code=400)

    result_query = User.query(User.email == email).get()

    if result_query is not None:
        return AdminResponse(text="User is already Created", response_code=400)

    if re.match(r"[^@]+@[^@]+\.[^@]+", email) is not None and isinstance(name, basestring) and isinstance(surname, basestring) and isinstance(is_admin, bool):

        if len(name) > 0 and len(surname) > 0 :
            new_user = User(email=email, name=name, surname=surname, is_admin=is_admin)
            new_user.put()
            return AdminResponse(text="User Created", response_code=200)
        return AdminResponse(text="All fields are mandatory", response_code=400)
    return AdminResponse(text="Invalid data found", response_code=400)

def delete_user(author, email, test=None):
    """
    Deletes an user with the provided data from the Client.
    The system will verify that the user is a valid Admin beforehand.
    The system will verify that the provided email exists in the database and that it's not the own user's email.
    """
    admin_email = author.email() if test is None else author.email

    if verify_admin_status(admin_email) is False:
        return AdminResponse(text="You don't have authorization to do this action", response_code=400)
    
    result_query = User.query(User.email == email).get()

    if result_query is None:
        return AdminResponse(text="User not found", response_code=400)

    if result_query.email == admin_email:
        return AdminResponse(text="You cannot delete yourself", response_code=400)

    result_query.key.delete()
    return AdminResponse(text="User Deleted", response_code=200)

def update_user(author, previous_email=None, email=None, name=None, surname=None, is_admin=None, test=None):
    """
    Updates the properties of an user with the provided data from the Client.
    The system will verify that the user is a valid Admin beforehand.
    This function also will be used to change the admin status of an user. An admin can't revoke said status from itself.
    """

    admin_email = author.email() if test is None else author.email

    if verify_admin_status(admin_email) is False:
        return AdminResponse(text="You don't have authorization to do this action", response_code=400)

    result_query = User.query(User.email == previous_email).get()

    if result_query is None:
        return AdminResponse(text="User not found", response_code=400)

    if admin_email == result_query.email and result_query.is_admin != is_admin:
        return AdminResponse(text="You cannot remove your admin privileges", response_code=400)
    if admin_email == result_query.email and result_query.email != email:
        return AdminResponse(text="You cannot change your admin email", response_code=400)

    result_query.email = email if re.match(r"[^@]+@[^@]+\.[^@]+", email) is not None else result_query.email
    result_query.name = name if isinstance(name, basestring) and len(name)>0 else result_query.name
    result_query.surname = surname if isinstance(surname, basestring) and len(surname)>0 else result_query.surname
    result_query.is_admin = is_admin if isinstance(is_admin, bool) else result_query.is_admin
    result_query.put()

    return AdminResponse(text="User Updated", response_code=200)

def get_all_users(author, test=None):
    """
    Returns all the users. The system will verify that the user is a valid Admin beforehand.
    """
    admin_email = author.email() if test is None else author.email

    if verify_admin_status(admin_email) is False:
        return AdminGetListUsersResponse(text="You don't have authorization to do this action", response_code=400)

    all_users = User.query()
    result = []
    for user in all_users:
        data_per_user = AdminCreateRequest(email=user.email,name=user.name, surname=user.surname, is_admin=user.is_admin)
        result.append(data_per_user)
    return AdminGetListUsersResponse(text="User List", response_code=200, users=result)

def verify_admin_status(user_email):
    """
    Verifies that the user has admin privileges. It will return True if it has a valid admin identificator.
    """
    is_an_admin = User.query(User.email == user_email).get()
    return False if is_an_admin is None else is_an_admin.is_admin 

