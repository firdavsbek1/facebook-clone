from django.utils import timezone
from rest_framework import permissions
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from rest_framework_simplejwt.views import TokenRefreshView

import api.serializers as serializers
from accounts.models import VIA_EMAIL, CodeVerification
from accounts.utils import send_email, send_sms


class LoginView(APIView):
    serializer_class = serializers.LoginSerializer
    permission_classes = [permissions.AllowAny, ]

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            return Response(serializer.data)
        return Response(serializer.errors)


class LogoutView(APIView):

    def post(self, request):
        refresh_token = RefreshToken(request.data.get('access_token'))
        refresh_token.blacklist()
        return Response({
            'success': True,
            'message': 'You have successfully logged out!'
        })


class VerifyTokenView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        token = request.data.get('token')
        if not token:
            raise ValidationError({'success': False, 'message': 'Token is required field. Send your token!'})
        try:
            access_token = AccessToken(token)
        except TokenError:
            access_token = None

        try:
            refresh_token = RefreshToken(token)
        except TokenError:
            refresh_token = None
        if access_token:
            token_type = 'access'
        else:
            token_type = 'refresh'
        return Response(data={
            'success': True,
            'Token type': token_type
        })


class RefreshTokenView(TokenRefreshView):

    def post(self, request, *args, **kwargs):
        data = {'success': True, 'access_token': super().post(request, *args, **kwargs).data['access']}
        return Response(data)


class SignUpAPIView(APIView):
    serializer_class = serializers.SignUpSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            code = user.get_verification_code()
            print(code)
            if user.auth_type == VIA_EMAIL:
                send_email(user.email, code=code)
            else:
                send_sms(user.phone_number, code=code)
            return Response(serializer.data)
        return Response(serializer.errors)


class CodeConfirmationView(APIView):
    serializer_class = serializers.CodeConfirmationSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            user = request.user
            confirmation_code = CodeVerification.objects.filter(
                code=serializer.validated_data.get('code'),
                user=user,
                expiration_time__gt=timezone.now(),
                is_confirmed=False
            )
            if confirmation_code.exists():
                confirmation_code.update(is_confirmed=True)
                refresh_token = RefreshToken.for_user(user)
                user.is_verified=True
                user.save()
                return Response({
                    'success': True,
                    'message': "You have successfully verified your account!",
                    'access_token':str(refresh_token.access_token),
                    'refresh_token': str(refresh_token),
                })
            raise ValidationError({
                'success': False,
                'message': "User confirmation failed! Your code expired or incorrect!"
            })
        return Response(serializer.errors)


class CodeResendView(APIView):

    def get(self,request):
        user=request.user
        if not user.is_verified:
            confirmation_code = user.codes.filter(
                expiration_time__gt=timezone.now(),
                is_confirmed=False
            )
            if confirmation_code.exists():
                return Response({
                    'success': False,
                    'message': "Your verification code is still valid. Use it to verify your account! "
                })
            code = user.get_verification_code()
            if user.auth_type == VIA_EMAIL:
                send_email(user.email, code)
            else:
                send_sms(user.phone_number, code)
            return Response({
                'success': True,
                'message': 'The confirmation code has been sent!'
            })
        return Response({
            'success': True,
            'message': 'Your account already verified! Go to login to get your token.'
        })

