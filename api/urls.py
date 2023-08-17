from django.urls import path
import api.views as views
from rest_framework.routers import DefaultRouter

router=DefaultRouter()
router.register('comments',views.CommentModelViewSet,'review')
router1=DefaultRouter()
router1.register('messages',views.MessageModelViewSetAPIView,'message')

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
    path('user/update/',views.ChangeUserInfoAPIView.as_view()),
    path('login/',views.LoginView.as_view()),
    path('logout/',views.LogoutView.as_view()),
    path('verify/',views.VerifyTokenView.as_view()),
    path('refresh/',views.RefreshTokenView.as_view()),
    path('code/confirmation/',views.CodeConfirmationView.as_view()),
    path('code/resend/',views.CodeResendView.as_view()),

    path('posts/',views.PostListCreateView.as_view()),
    path('posts/<uuid:post_id>/',views.PostRetRetrieveUpdateDestroyAPIView.as_view()),
    # path('comments/',views.CommentListCreateAPIView.as_view()),
    # path('messages/',views.MessageListCreateAPIView.as_view()),

    path('like/',views.PostLikeAPIView.as_view()),
    path('upvote/',views.UpvoteAPIView.as_view()),
    path('downvote/',views.DownVoteAPIView.as_view()),


]

urlpatterns+=router.urls
urlpatterns+=router1.urls
