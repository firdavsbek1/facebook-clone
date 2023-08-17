from django.contrib import admin
from .models import CustomUser,FriendList,FriendRequest,CodeVerification


class CustomUserAdmin(admin.ModelAdmin):
    list_display = ['username','first_name','last_name','email']


admin.site.register(CustomUser,CustomUserAdmin)
admin.site.register(FriendList)
admin.site.register(FriendRequest)
admin.site.register(CodeVerification)
