from django.db.models.signals import post_save
from accounts.models import CustomUser, FriendList


def create_friend_list(sender,instance,created,**kwargs):
    if created:
        FriendList.objects.create(user=instance)


post_save.connect(create_friend_list,sender=CustomUser)