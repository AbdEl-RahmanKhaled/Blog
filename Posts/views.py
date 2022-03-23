from pyexpat.errors import messages

from django.shortcuts import render
from django.views import View
from .models import Post
from Accounts.models import Account
from Comments.models import Comment
from Posts.models import Post, PostLikes, PostDislikes, Category
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from Helpers.Decorators.auth_decorators import verified_acc_only


def index(request):
    return render(request, '_layout.html')


@login_required(redirect_field_name=None, login_url='/account/login')
@verified_acc_only
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


def like(request):
    if request.method == 'POST':
        post = Post.objects.get(id=request.POST['p_id'])
        post_likes = PostLikes.objects.filter(account_id=request.user.id, post=post)
        post_dislikes = PostDislikes.objects.filter(account_id=request.user.id, post=post)

        if post_likes.exists():
            post.likes -= 1
            post_likes.delete()
            post.save()

        else:

            if post_dislikes.exists():
                post_dislikes.delete()
                post.dislikes -= 1

            new_like = PostLikes(account_id=request.user.id, post=post)
            post.likes += 1
            new_like.save()
            post.save()

    return redirect('postDetails', p_id=request.POST['p_id'])


def dislikes(request):
    post = Post.objects.get(id=request.POST['p_id'])
    post_dislikes = PostDislikes.objects.filter(account_id=request.user.id, post=post)
    post_likes = PostLikes.objects.filter(account_id=request.user.id, post=post)

    if post_dislikes.exists():
        post.dislikes -= 1
        post_dislikes.delete()
        post.save()
    else:

        if post_likes.exists():
            post_likes.delete()
            post.likes -= 1

        new_dislike = PostDislikes(account_id=request.user.id, post=post)
        post.dislikes += 1
        new_dislike.save()
        post.save()
    return redirect('postDetails', p_id=request.POST['p_id'])

def sub_category(request, cat_id):
    account = Account.objects.get(id=request.user.id)
    cat = Category.objects.get(id=cat_id)
    # subbed_cat = account.objects.filter(subbed_users__category=cat)
    # if not subbed_cat.exists():
    cat.subbed_users.add(account)
    return redirect(posts)

def unsub_category(request, cat_id):
    account = Account.objects.get(id=request.user.id)
    cat = Category.objects.get(id=cat_id)
    # subbed_cat = account.objects.filter(subbed_users__category=cat)
    # if not subbed_cat.exists():
    cat.subbed_users.remove(account)
    return redirect(posts)


# admin modules

class PostsAdminView(View):
    template = 'posts/admin-posts.html'

    def get(self, request):
        context = {
            'posts': Post.objects.all()
        }
        return render(request, self.template, context)


# def PostsAdminView(request):
#     # template = 'admin-posts.html'
#     posts = Post.objects.all()
#     context = {"object_list": posts}
#     return render(request, 'posts/admin-posts.html', context)


class PostEditAdmin(View):
    template = 'posts/adminEditPost.html'

    def get(self, request, p_id):
        context = {
            'post': Post.objects.get(id=p_id)
        }
        return render(request, self.template, context)

    def post(self, request):
        # request.POST.pop('csrfmiddlewaretoken')
        print(request.POST)
        post = Post(**request.POST)
        post.save()
        return redirect('index')

