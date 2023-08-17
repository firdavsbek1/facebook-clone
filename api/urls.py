from django.urls import path,include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView,TokenVerifyView,TokenBlacklistView

import api.views as views
urlpatterns=[
    # 3rd Party authentication
    # path('auth/',include('allauth.urls')),
    # path('auth/dj-rest/',include('dj_rest_auth.urls')),
    # path('auth/dj-rest/registration',include('dj_rest_auth.registration.urls')),

    # TokenObtainPair,TokenRefresh
    # path('login/',TokenObtainPairView.as_view()),
    # path('refresh/',TokenRefreshView.as_view()),
    # path('verify/',TokenVerifyView .as_view()),
    # path('logout/',TokenBlacklistView .as_view()),

    # local jwt authentication
    path('signup/',views.SignUpAPIView.as_view()),
    path('login/',views.LoginView.as_view()),
    path('logout/',views.LogoutView.as_view()),
    path('verify/',views.VerifyTokenView.as_view()),
    path('refresh/',views.RefreshTokenView.as_view()),
    path('code/confirmation/',views.CodeConfirmationView.as_view()),
    path('code/resend/',views.CodeResendView.as_view()),


]
