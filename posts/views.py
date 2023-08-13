from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404

from .forms import CommentForm
from .models import Post, Review, PostLike, UpVote, DownVote


@login_required
def post_create(request):
    if request.method == "POST":
        data=request.POST
        post=Post.objects.create(content=data.get('content'),post_image=request.FILES.get('photo'),author=request.user)
        return redirect('landing-page')
    return render(request, 'posts/post.html')


@login_required
def comment_create(request,post_id):
    comments = Review.objects.filter(post_id=post_id).order_by('-created_time')
    post = get_object_or_404(Post,id=post_id)

    if request.method == "POST":
        form=CommentForm(data=request.POST)
        if form.is_valid():
            review=form.save(commit=False)
            review.author=request.user
            review.post=post
            review.save()
            return redirect('comment-create',post_id=post.id)
    return render(request, 'posts/comment.html',{'comments':comments,'post':post})


def comment_delete(request,comment_id):
    comment=get_object_or_404(Review,id=comment_id)
    post=comment.post
    if request.method == 'POST':
        comment.delete()
        return redirect('comment-create',post_id=post.id)
    return render(request,'posts/delete.html',context={'comment':comment,'post':post})


def comment_edit(request,comment_id):
    comment=get_object_or_404(Review,id=comment_id)
    post=comment.post
    if request.method == 'POST':
        form=CommentForm(instance=comment,data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('comment-create',post_id=post.id)
    return render(request,'posts/comment.html',context={'comment':comment,'post':post,'edit':True})


@login_required
def post_like(request,post_id):
    post=Post.objects.get(id=post_id)
    user=request.user
    like,created=PostLike.objects.get_or_create(post=post,user=user)
    if not created:
        like.delete()
    return redirect('landing-page')


@login_required
def up_vote(request,comment_id):
    comment=Review.objects.get(id=comment_id)
    upvote=UpVote.objects.filter(comment_id=comment_id)
    downvote = DownVote.objects.filter(comment_id=comment_id,user=request.user)
    if not (upvote.exists() or downvote.exists()):
        comment.update_vote_total()
    if not upvote.exists():
        UpVote.objects.create(user=request.user,comment=comment)
        comment.update_upvote()
    if downvote.exists():
        downvote.delete()

    comment.save()

    return redirect('comment-create',post_id=comment.post.id)


@login_required
def down_vote(request,comment_id):
    comment=Review.objects.get(id=comment_id)
    downvote=DownVote.objects.filter(comment_id=comment_id,user=request.user)
    upvote = UpVote.objects.filter(comment_id=comment_id,user=request.user)
    if not (upvote.exists() or downvote.exists()):
        comment.update_vote_total()
    if not downvote.exists():
        DownVote.objects.create(user=request.user,comment=comment)
    if upvote.exists():
        upvote.delete()
        comment.up_vote-=1
    comment.save()

    return redirect('comment-create',post_id=comment.post.id)