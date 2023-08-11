from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.urls import path, include
from posts.models import Post


@login_required
def landing_page(request):
    posts=Post.objects.all().order_by('-created_time')
    return render(request, 'landing-page.html',{'posts':posts})


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', landing_page, name='landing-page'),
    path('accounts/', include('accounts.urls')),
    path('posts/', include('posts.urls')),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
