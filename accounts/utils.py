import re
import threading

from django.conf import settings
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from enum import Enum

from django.core.mail import send_mail

from accounts.models import FriendRequest
from twilio.rest import Client

EMAIL_REGEX = r"^[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*@(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)" \
              r"+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?$"
PHONE_REGEX="^\\+?[1-9][0-9]{7,14}$"
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


class EmailThread(threading.Thread):
    def __init__(self,subject,message,recipient_list):
        self.subject = subject
        self.message = message
        self.recipient_list = recipient_list
        super().__init__()

    def run(self):
        send_mail(
            subject=self.subject,
            message=self.message,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=self.recipient_list
        )


def send_email(user_email,code):
    thread=EmailThread(
        subject='Confirmation Code To FaceBook Like!',
        message=f"Your confirmation code is {code}, Use it to verify your account!",
        recipient_list=[user_email]
    )
    thread.start()


client=Client("account_sid", "auth_token")


def send_sms(user_phone,code):
    client.messages.create(
        to=user_phone,
        from_='+998908790987',
        body=f"Your confirmation code is {code}, Use it to verify your account!",
    )

