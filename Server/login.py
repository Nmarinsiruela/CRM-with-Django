import datetime

from messages import LoginResponse
from models import User

def log_in(user, name, surname, test=None):
    """
    A function which validates the login. For developing purposes, it creates a new User if it doesn't exist.
    If it's a returning user, this function returns the stored data.
    Needs - User verified by Google.
    """
    if user is None:
        return LoginResponse(text="Error. Invalid Data", response_code= 400)
    else:
        if test is None:
            email = user.email()
        else:
            email = user.email

        valid_user = User.query(User.email == email).get()
        if valid_user is None:
            new_user = User(email=email, name=name, surname=surname, is_admin=False)
            new_user.put()
            return LoginResponse(text="New Login", name=new_user.name, surname=new_user.surname, is_admin=new_user.is_admin, response_code=200)
            # return LoginResponse(text="Error. User not found", response_code= 400)
        else:
            return LoginResponse(text="Correct Login", response_code=200, name=valid_user.name, surname=valid_user.surname, is_admin=valid_user.is_admin)