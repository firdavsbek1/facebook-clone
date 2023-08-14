import datetime
from itertools import chain
from operator import attrgetter
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import render
from django.urls import path, include
from accounts.models import CustomUser
from posts.models import Post, Story


@login_required
def landing_page(request):
    user = CustomUser.objects.get(id=request.user.id)
    queryset = user.friend_list.friends.all()
    posts = Post.objects.filter(author__in=queryset).order_by('-created_time')
    post_likes = user.likes.all()
    posts_liked = [like.post for like in post_likes]
    stories = Story.objects.filter(
        user__in=queryset,
        expiration_time__gte=datetime.datetime.now()).order_by('-created_time')
    return render(request, 'landing-page.html',
                  {'posts': posts, 'posts_liked': posts_liked, 'stories': stories})


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', landing_page, name='landing-page'),
    path('accounts/', include('accounts.urls')),
    path('posts/', include('posts.urls')),
    path('messages/',include('messages_app.urls')),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
