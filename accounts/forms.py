from django import forms

from accounts.models import CustomUser


class UserForm(forms.ModelForm):
    password = forms.CharField(required=False)
    bio = forms.CharField(required=False)

    class Meta:
        model = CustomUser
        fields = "__all__"
        exclude = ('id',
                   'gender',
                   'role',
                   'first_name',
                   'last_name',
                   'date_joined',
                   'date_of_birth',
                   'is_active',
                   'is_staff',
                   'is_superuser',
                    'user_permissions',
                   'last_login'
                   )


class UploadImageForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields=('cover_image',)