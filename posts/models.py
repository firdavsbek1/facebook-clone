import uuid
from django.db import models
from django.db.models import UniqueConstraint

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
    up_vote=models.IntegerField(default=0)
    vote_total=models.IntegerField(default=0)

    created_time=models.DateTimeField(auto_now_add=True)
    updated_time=models.DateTimeField(auto_now=True)

    def update_upvote(self):
        self.up_vote+=1

    def update_vote_total(self):
        self.vote_total+=1

    def __str__(self):
        return self.comment[:50]


class PostLike(models.Model):
    post = models.ForeignKey(Post,on_delete=models.CASCADE,related_name='likes')
    user = models.ForeignKey(CustomUser,on_delete=models.CASCADE,related_name='likes')

    class Meta:
        constraints=[
            UniqueConstraint(
                name="OneLikePerPostPerUser",
                fields=['post','user']
            )
        ]

    def __str__(self):
        return self.user.username + " liked the post: "+self.post.content[:50]


class UpVote(models.Model):
    user=models.ForeignKey(CustomUser,on_delete=models.CASCADE,related_name='upvotes')
    comment=models.ForeignKey(Review,on_delete=models.CASCADE,related_name='upvotes')

    class Meta:
        constraints=[
            UniqueConstraint(
                name="OneLikeOneUpVotePerUser",
                fields=['user','comment']
            )
        ]


class DownVote(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='down_votes')
    comment = models.ForeignKey(Review, on_delete=models.CASCADE, related_name='down_votes')

    class Meta:
        constraints = [
            UniqueConstraint(
                name="OneLikeOneDownVotePerUser",
                fields=['user', 'comment']
            )
        ]


class Story(models.Model):
    user=models.ForeignKey(CustomUser,on_delete=models.CASCADE,related_name='stories')
    story_image=models.ImageField(upload_to='images/story/images/',null=True,blank=True)
    created_time=models.DateTimeField(auto_now_add=True)

