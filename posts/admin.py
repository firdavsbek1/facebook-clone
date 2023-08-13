from django.contrib import admin
from .models import Post,Review,PostLike,UpVote,DownVote,Story


admin.site.register(Post)
admin.site.register(Review)
admin.site.register(PostLike)
admin.site.register(UpVote)
admin.site.register(DownVote)
admin.site.register(Story)
# Register your models here.
