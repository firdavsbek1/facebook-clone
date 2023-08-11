import re
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from enum import Enum
from accounts.models import FriendRequest

EMAIL_REGEX = r"^[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*@(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)" \
              r"+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?$"
PHONE_REGEX=r"^\\+?[1-9][0-9]{7,14}$"
USERNAME_REGEX='^(?=.{4,32}$)(?![_.-])(?!.*[_.]{2})[a-zA-Z0-9._-]+(?<![_.])$'
MESSAGE_TEMPLATE={
    'success':True,
    'message':''
}

def validate_email(email):
    return re.match(EMAIL_REGEX,email)


def validate_phone_number(phone_number):
    return re.match(PHONE_REGEX,phone_number)


def validate_username(username):
    return re.match(USERNAME_REGEX,username)


def justify_input_type(user_input):
    if validate_email(user_input):
        return 'email'
    elif validate_phone_number(user_input):
        return 'phone'
    elif validate_username(user_input):
        return 'username'
    else:
        return False


def validate_fields(*args):
    for item in args:
        if item is None:
            return False
    return True


def check_new_password(password1,password2):
    if password2 and password1:
        if password1 == password2:
            try:
                validate_password(password1)
            except ValidationError as error:
                MESSAGE_TEMPLATE.update(message=error,success=False)
        else:
            MESSAGE_TEMPLATE.update(message='New Password Confirmation Failed. Not match!', success=False)
    elif password1 or password2:
        MESSAGE_TEMPLATE.update(message='Please, enter both Password and Password Confirmation!', success=False)
    return MESSAGE_TEMPLATE


def validate_full_name(full_name):
    first_name,surname=full_name.split()
    return first_name,surname


def get_friend_request_or_false(sender,receiver):
    requests=FriendRequest.objects.filter(sender=sender,receiver=receiver,is_active=True)
    if requests.exists():
        return requests.first()
    return False


class RequestFriendStatus(Enum):
    NO_REQUEST_SENT=-1
    THEM_SENT_YOU=0
    YOU_SENT_THEM=1


