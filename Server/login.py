from messages import LoginResponse
from models import User

def log_in(user, name, surname, test=None):
    """
    A function which validates the login. For developing purposes, it creates a new User if it doesn't exist.
    If it's a returning user, this function returns the stored data.
    Needs - User verified by Google.
    """

    # This protects the system in case an invalid petition from the Client is made.
    if user is None:
        return LoginResponse(text="Error. Invalid Data", response_code= 400)
    else:
        
        # Condition to enable the tests. Endpoints requires a email() method, but the User model tested has email as an attribute.
        email = user.email() if test is None else user.email

        # Query to look for a valid email.
        valid_user = User.query(User.email == email).get()

        # If the User doesn't exist, it'll be considered an invalid access.
        if valid_user is None:
            # A special case is evaluated in order to develop. This will be erased in production.
            if email != 'nmarinsiruela@gmail.com':
                return LoginResponse(text="Error. Invalid user detected", response_code= 400)
            else:
                new_user = User(email=email, name=name, surname=surname, is_admin=True)
                new_user.put()
                return LoginResponse(text="Special user created", name=new_user.name, surname=new_user.surname, is_admin=new_user.is_admin, response_code=200)
        else:
            return LoginResponse(text="Correct Login", response_code=200, name=valid_user.name, surname=valid_user.surname, is_admin=valid_user.is_admin)