import datetime
from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework_simplejwt.tokens import RefreshToken

from accounts.models import VIA_EMAIL, VIA_PHONE
from .models import CustomUser
from accounts.utils import justify_input_type, send_email

MESSAGE_TEMPLATE = {
    'success': False,
    'message': ''
}


class LoginSerializer(serializers.Serializer):
    user_input = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user_input = data.get('user_input')
        input_type = justify_input_type(user_input)
        if input_type:
            if input_type == 'email':
                user = CustomUser.objects.filter(email__iexact=user_input)
            elif input_type == 'phone':
                user = CustomUser.objects.filter(phone_number=user_input)
            else:
                user = CustomUser.objects.filter(username__iexact=user_input)
            if user.exists():
                user_authenticated = authenticate(username=user.first().username, password=data.get('password'))
                if user_authenticated:
                    token = RefreshToken.for_user(user.first())
                    data['access_token'] = str(token.access_token)
                    data['refresh_token'] = str(token)
                    return data
                else:
                    MESSAGE_TEMPLATE.update(
                        message='User can\'t be authenticated with the given credentials!')
            else:
                MESSAGE_TEMPLATE.update(
                    message='User with that credentials not found!')
        else:
            MESSAGE_TEMPLATE.update(
                message='Your input value was not identified as email/phone_number or username.Try again!')
        raise ValidationError(MESSAGE_TEMPLATE)

    def to_representation(self, instance):
        data = {
            'access_token': str(instance.get('access_token')),
            'refresh_token': str(instance.get('refresh_token'))
        }
        return data


class SignUpSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)
    phone_number_or_email = serializers.CharField(required=True,write_only=True)
    date_of_birth = serializers.DateField()
    gender = serializers.CharField(required=True)
    password=serializers.CharField(write_only=True)
    auth_type=serializers.CharField(read_only=True)

    class Meta:
        model = CustomUser
        fields=('id','first_name','last_name','email','phone_number',
                'date_of_birth','gender','password','phone_number_or_email','auth_type')

    def validate_password(self, password):
        validate_password(password)
        return password

    def validate_gender(self, gender):
        if not gender.lower() in ['male', 'female']:
            raise ValidationError({'success': False, 'message': 'Please enter valid gender nouns(male&female)!'})
        return gender

    def validate_date_of_birth(self, date_of_birth):
        if date_of_birth.year >= datetime.date.today().year:
            MESSAGE_TEMPLATE.update(message='Date of Birth field was not filled appropriately!')
            raise ValidationError(MESSAGE_TEMPLATE)
        return date_of_birth

    def validate(self, attrs):
        input_type = justify_input_type(attrs.get('phone_number_or_email'))
        if input_type == 'email':
            if CustomUser.objects.filter(email__iexact=attrs.get('phone_number_or_email')).exists():
                MESSAGE_TEMPLATE.update(message="That email was already used. Go to login or try with another one!")
                raise ValidationError(MESSAGE_TEMPLATE)
            attrs['email'] = attrs.get('phone_number_or_email')
            attrs['auth_type'] = VIA_EMAIL
        elif input_type == 'phone':
            if CustomUser.objects.filter(phone_number=attrs.get('phone_number_or_email')).exists():
                MESSAGE_TEMPLATE.update(
                    message="That phone number was already used. Go to login or try with another one!")
                raise ValidationError(MESSAGE_TEMPLATE)
            attrs['phone_number'] = attrs.get('phone_number_or_email')
            attrs['auth_type'] = VIA_PHONE
        else:
            MESSAGE_TEMPLATE.update(message='Invalid phone_number or email entered!')
            raise ValidationError(MESSAGE_TEMPLATE)
        return attrs

    def create(self, validated_data):
        contact_info=validated_data.pop('phone_number_or_email')
        user=CustomUser.objects.create_user(
            username=contact_info,
            password=validated_data.get('password'),
            first_name=validated_data.get('first_name'),
            last_name=validated_data.get('last_name'),
            email=validated_data.get('email'),
            phone_number=validated_data.get('phone_number'),
            date_of_birth=validated_data.get('date_of_birth'),
            gender=validated_data.get('gender').title(),
            auth_type=validated_data.get('auth_type'),
        )
        return user

    def to_representation(self, instance):
        refresh_token=RefreshToken.for_user(instance)
        data={
            'success':True,
            'message':'Account confirmation code has been sent! Go ahead and verify your account!',
            'access_token':str(refresh_token.access_token),
            'refresh_token':str(refresh_token),
            'user_info':super().to_representation(instance)
        }
        return data


class CodeConfirmationSerializer(serializers.Serializer):
    code=serializers.CharField(max_length=6,write_only=True)

