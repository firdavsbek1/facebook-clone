from django.urls import path
import posts.views as views

urlpatterns=[
    path('',views.post_create,name='post-create'),
    path('<uuid:post_id>/like/',views.post_like,name='post-like'),
    path("<uuid:post_id>/comments/create/",views.comment_create,name='comment-create'),
    path("comments/<uuid:comment_id>/upvote/",views.up_vote,name='comment-upvote'),
    path("comments/<uuid:comment_id>/downvote/",views.down_vote,name='comment-downvote'),
    path("comments/<uuid:comment_id>/delete/",views.comment_delete,name='comment-delete'),
    path("comments/<uuid:comment_id>/edit/",views.comment_edit,name='comment-edit'),
]
