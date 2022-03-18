from django.contrib.auth.models import User
from django.shortcuts import render
from Accounts.models import Account
from Comments.models import Comment
from Posts.models import Post, PostLikes, PostDislikes
from django.shortcuts import redirect
from django.http import HttpResponseRedirect
from django.urls import reverse


# Create your views here.

def index(request):
    return render(request, '_layout.html')


def posts(request):
    post = Post.objects.all().order_by('-date')
    context = {"posts": post}
    return render(request, 'posts/timeline.html', context)


def post_detail(request, p_id):
    post = Post.objects.get(id=p_id)
    comments = Comment.objects.filter(post=post)
    context = {
        'post': post,
        'comments': comments
               }
    return render(request, 'posts/Post_detail.html', context)


def like(request, p_id):
    account = Account.objects.get(id=request.user.id)
    post = Post.objects.get(id=p_id)
    post_likes = PostLikes.objects.filter(account=account, post=post)
    post_dislikes = PostDislikes.objects.filter(account=account, post=post)

    if post_likes.exists():
        post.likes -= 1
        post_likes.delete()
        post.save()

    else:

        if post_dislikes.exists():
            post_dislikes.delete()
            post.dislikes -= 1

        newLike = PostLikes(account=account, post=post)
        post.likes += 1
        newLike.save()
        post.save()

    return redirect('postDetails', p_id=p_id)


def dislikes(request, p_id):
    account = Account.objects.get(id=request.user.id)
    post = Post.objects.get(id=p_id)
    post_dislikes = PostDislikes.objects.filter(account=account, post=post)
    post_likes = PostLikes.objects.filter(account=account, post=post)

    if post_dislikes.exists():
        post.dislikes -= 1
        post_dislikes.delete()
        post.save()
    else:

        if post_likes.exists():
            post_likes.delete()
            post.likes -= 1

        newDislike = PostDislikes(account=account, post=post)
        post.dislikes += 1
        newDislike.save()
        post.save()
    return redirect('postDetails', p_id=p_id)
    # return HttpResponseRedirect("/Post_detail/" + p_id)
