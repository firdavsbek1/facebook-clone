from django.urls import path
import accounts.views as views

app_name='accounts'
urlpatterns=[
    path('login/',views.login_view,name='login'),
    path('logout/',views.logout_view,name='logout'),
    path('register/',views.register_view,name='register'),
    # path('profile/',views.profile_page,name='profile'),
    path('profile/edit/',views.profile_edit,name='profile-edit'),
    path('<int:pk>/profile/',views.profile_page,name='profile'),

    # friend reqeust handling
    path('friend-request/<int:friend_id>/unfriend/',views.trigger_unfriend,name='trigger-unfriend'),
    path('friend-request/<int:friend_id>/send/',views.trigger_request,name='trigger-reqeust'),
    path('friend-request/<int:friend_id>/cancel/',views.trigger_cancel,name='trigger-cancel'),
    path('friend-request/<int:request_id>/accept/',views.trigger_accept,name='trigger-accept'),
    path('friend-request/<int:request_id>/decline/',views.trigger_decline,name='trigger-decline'),
]