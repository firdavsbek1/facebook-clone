from django.urls import path
import messages_app.views as views

urlpatterns=[
    path('t/<int:user_id>/',views.message,name='message-to')
]