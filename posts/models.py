import uuid
from django.db import models
from accounts.models import CustomUser


class Post(models.Model):
    author=models.ForeignKey(CustomUser,on_delete=models.CASCADE,related_name='posts')
    content=models.TextField()
    post_image=models.ImageField(upload_to='posts/images',null=True,blank=True)

    created_time=models.DateTimeField(auto_now_add=True)
    updated_time=models.DateTimeField(auto_now=True)
    id=models.UUIDField(default=uuid.uuid4,primary_key=True,editable=False)

    def __str__(self):
        return self.content[:50]


# class Story(models.Model):
#     author = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='posts')
#     story_media = models.ImageField(upload_to='story/images')
#
#     created_time = models.DateTimeField(auto_now_add=True)
#     id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)


class Review(models.Model):
    id=models.UUIDField(default=uuid.uuid4,primary_key=True,editable=False)
    author=models.ForeignKey(CustomUser,on_delete=models.CASCADE,related_name='reviews')
    post=models.ForeignKey(Post,on_delete=models.CASCADE,related_name='reviews')
    comment=models.TextField()
    parent=models.ForeignKey('Review',on_delete=models.SET_NULL,null=True,blank=True,related_name='children')

    created_time=models.DateTimeField(auto_now_add=True)
    updated_time=models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.comment[:50]