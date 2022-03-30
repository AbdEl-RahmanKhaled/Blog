from django.core.paginator import Paginator
from django.shortcuts import render
from Accounts.models import Account
from Comments.models import Comment
from Posts.models import Post, PostLikes, PostDislikes, Category
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from Helpers.Decorators.auth_decorators import verified_acc_only
from django.db.models import Q


def index(request):
    return render(request, '_layout.html')


def posts(request):
    post = Post.objects.all().order_by('-date')
    subbed_unsubbed = get_cat(request)
    if request.user.is_authenticated:
        post = Post.objects.filter(category__in=list(subbed_unsubbed["subbed_cat"].values_list('id', flat=True)))

    paginator = Paginator(post, 5)
    page = request.GET.get('page')
    page_posts = paginator.get_page(page)
    context = {"posts": page_posts}
    context.update(subbed_unsubbed)
    return render(request, 'posts/timeline.html', context)


def post_detail(request, p_id):
    post = Post.objects.get(id=p_id)
    comments = Comment.objects.filter(post=post).order_by('-created_on')
    subbed_unsubbed = get_cat(request)
    context = {
        'post': post,
        'comments': comments}
    context.update(subbed_unsubbed)
    return render(request, 'posts/Post_detail.html', context)


@login_required(redirect_field_name=None, login_url='/account/login')
@verified_acc_only
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


@login_required(redirect_field_name=None, login_url='/account/login')
@verified_acc_only
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


@login_required(redirect_field_name=None, login_url='/account/login')
@verified_acc_only
def sub_category(request, cat_id):
    print("inside sub")
    account = Account.objects.get(id=request.user.id)
    cat = Category.objects.get(id=cat_id)
    cat.subbed_users.add(account)
    return redirect(posts)


@login_required(redirect_field_name=None, login_url='/account/login')
@verified_acc_only
def unsub_category(request, cat_id):
    account = Account.objects.get(id=request.user.id)
    cat = Category.objects.get(id=cat_id)
    cat.subbed_users.remove(account)
    return redirect(posts)


def search(request):
    searched = request.GET['searched']
    post = Post.objects.filter(Q(title__icontains=searched) | Q(category__category__icontains=searched))
    paginator = Paginator(post, 5)
    page = request.GET.get('page')
    page_posts = paginator.get_page(page)

    subbed_unsubbed = get_cat(request)

    context = {"posts": page_posts}
    context.update(subbed_unsubbed)
    return render(request, 'posts/search_result.html', context)


def get_cat(request):
    unsubbed_cat = Category.objects.all()
    subbed_cat = []
    if request.user.is_authenticated:
        subbed_cat = Account.objects.get(pk=request.user.id).accounts.all()
        unsubbed_cat = Category.objects.exclude(category__in=list(subbed_cat.values_list('category', flat=True)))

    return {"subbed_cat": subbed_cat,
            "unsubbed_cat": unsubbed_cat}
