import uuid
from datetime import timezone

from django.contrib.auth import authenticate
from django.contrib.auth.models import AbstractUser
from django.db import models

NOT_SPECIFIED, MALE, FEMALE, OTHER = ('N', 'M', 'F', 'O')
ORDINARY, ADMIN, ADMINISTRATOR, SUPERUSER = ('ORDINARY', 'ADMIN', 'ADMINISTRATOR', 'SUPERUSER')

GENDER = (
    (NOT_SPECIFIED, "Not specified"),
    (MALE, "Male"),
    (FEMALE, "Female"),
    (OTHER, "Other"),
)

ROLES = (
    (ORDINARY, "Ordinary"),
    (ADMIN, "Admin"),
    (ADMINISTRATOR, "Administrator"),
    (SUPERUSER, "Superuser"),
)


class CustomUser(AbstractUser):
    phone_number = models.CharField(max_length=18, null=True)
    profile_image = models.ImageField(default='accounts/images/user-default.png', upload_to='accounts/images/')
    date_of_birth = models.DateField(null=True)
    gender = models.CharField(max_length=1, choices=GENDER, default=OTHER)
    role = models.CharField(max_length=16, choices=ROLES, default=ORDINARY)

    from_location = models.CharField(max_length=200, null=True, blank=True)
    lives = models.CharField(max_length=200, null=True, blank=True)
    marriage_status = models.CharField(max_length=200, null=True, blank=True)
    studied = models.CharField(max_length=200, null=True, blank=True)
    works_at = models.CharField(max_length=200, null=True, blank=True)
    bio = models.TextField(null=True)
    website=models.CharField(max_length=200,null=True,blank=True)
    cover_image=models.ImageField(upload_to='accounts/images/',default='accounts/images/default-cover.svg')

    # for messaging
    last_message_time=models.DateTimeField(null=True,blank=True)

    def validate_username(self, new_username):
        if self.username != new_username:
            user = CustomUser.objects.filter(username__iexact=new_username)
            if user.exists():
                return False
            self.username = new_username
        return True

    def validate_password(self, password):
        user = authenticate(username=self.username, password=password)
        if user:
            return True
        return False

    def set_username(self):
        if self.username == self.first_name.lower()+'default':
            self.username = f"{self.username}-{uuid.uuid4()[:10]}"
            self.save()

    def clean(self):
        self.set_username()

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.clean()

    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    def __str__(self):
        return self.username

    # id=models.UUIDField(default=uuid.uuid4(),primary_key=True)
    last_activity = models.DateTimeField(auto_now_add=True, null=True)
    updated_time = models.DateTimeField(auto_now=True, null=True)


class FriendList(models.Model):
    user=models.OneToOneField(CustomUser,on_delete=models.CASCADE,related_name='friend_list')
    friends=models.ManyToManyField(CustomUser,related_name='friends')

    def __str__(self):
        return self.user.username

    def add_friend(self,account):
        if not account in self.friends.all():
            self.friends.add(account)
            self.save()

    def remove_friend(self,account):
        if account in self.friends.all():
            self.friends.remove(account)
            self.save()

    def unfriend(self,removee):
        self.remove_friend(removee)
        removee_friend_list=FriendList.objects.get(user=removee)
        removee_friend_list.remove_friend(self.user)

    def is_mutual_friend(self,friend):
        if friend in self.friends.all():
            return True
        return False


class FriendRequest(models.Model):
    sender=models.ForeignKey(CustomUser,on_delete=models.CASCADE,related_name='sent_requests')
    receiver=models.ForeignKey(CustomUser,on_delete=models.CASCADE,related_name='received_requests')
    is_active=models.BooleanField(default=True,null=True,blank=True)
    created_time=models.DateTimeField(auto_now_add=True)

    def accept(self):
        sender_friend_list=FriendList.objects.get(user=self.sender)
        if sender_friend_list:
            sender_friend_list.add_friend(self.receiver)
            receiver_friend_list=FriendList.objects.get(user=self.receiver)
            receiver_friend_list.add_friend(self.sender)
            self.is_active=False
            self.save()

    def decline(self):
        self.is_active=False
        self.save()

    def cancel(self):
        self.is_active=False
        self.save()

