from django.shortcuts import render
from Accounts.models import Account
from Helpers.Decorators.auth_decorators import *
from django.views import View
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from Posts.models import Post
from .forms import PostForm


# Create your views here.
# admin views
class AllUsersView(View):
    @method_decorator([login_required, superuser_required])
    def get(self, request):
        context = {
            'users': Account.objects.all()
        }
        return None


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
    post = None

    def get(self, request, p_id):
        self.post = Post.objects.get(p_id)
        post = PostForm(instance=self.post)
        context = {'post': post}
        return render(request, self.template, context)

    def post(self, request):
        # post = Post(**request.POST)
        # post.save()
        return redirect('admin-posts')


# class PostDeleteAdmin(View):
#     def post(self, request):
#         try:
#             post = Post.objects.get(request.POST['p_id'])
#             post.delete()
#         except Exception:
#             messages.error(request, 'Not valid post id')
#         return redirect('admin-posts')


def PostDeleteAdmin(request, p_id):
    post = Post.objects.get(id=p_id)
    post.delete()
    return redirect('admin-posts')


def AddPostAdmin(request):
    post = PostForm()
    # template = 'posts/admin-Posts.html'
    context = {'post': post}
    return render(request, 'posts/adminAddPost.html', context)
