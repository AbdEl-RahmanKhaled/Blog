from django.shortcuts import render
from django.urls import reverse
from django.views.generic import UpdateView, CreateView

from Accounts.models import Account
from Helpers.Decorators.auth_decorators import *
from django.views import View
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator


# Create your views here.
# admin views
from ManageBlog.forms import UserForm, PostForm
from Posts.models import Post


class AllUsersView(View):
    # @method_decorator([login_required, superuser_required])
    def get(self, request):
        context = {
            'users': Account.objects.all()
        }
        return render(request, 'manage_blog/users/users-list.html', context)


class EditUserView(UpdateView):
    model = Account
    fields = ('first_name', 'last_name', 'username', 'email', 'is_superuser', 'phone_number', 'gender')
    # fields = '__all__'
    template_name = 'manage_blog/users/edit-user-form.html'

    def get_success_url(self):
        return reverse('admin_users_list')


class CreateUserView(CreateView):
    form_class = UserForm
    template_name = 'manage_blog/users/add-user-form.html'

    def get_success_url(self):
        return reverse('admin_users_list')

    def form_valid(self, form):
        form.instance.set_password(form.cleaned_data['password'])
        return super().form_valid(form)


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
