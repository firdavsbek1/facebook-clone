from django.db import models

from accounts.models import CustomUser


class Message(models.Model):
    message_sender=models.ForeignKey(CustomUser,on_delete=models.CASCADE,related_name='messages_sent')
    message_receiver=models.ForeignKey(CustomUser,on_delete=models.CASCADE,related_name='messages_received')
    content=models.CharField(max_length=250,null=True,blank=True)
    is_owner=models.BooleanField(default=False)

    created_time=models.DateTimeField(auto_now_add=True)
    updated_time=models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.content[:50]
