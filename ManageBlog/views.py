from django.shortcuts import render
from django.urls import reverse
from django.views.generic import UpdateView, CreateView
from Accounts.models import Account
from Helpers.Decorators.auth_decorators import *
from django.views import View
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from ManageBlog.forms import UserForm, PostForm
from Posts.models import Post
from django.core.paginator import Paginator


class AllUsersView(View):
    @method_decorator([login_required(redirect_field_name=None, login_url='/account/login'), superuser_required])
    def get(self, request):
        users = Account.objects.all().order_by('-date_joined')
        paginator = Paginator(users, 7)
        page = request.GET.get('page')
        page_users = paginator.get_page(page)
        context = {
            'users': page_users
        }
        return render(request, 'manage_blog/users/users-list.html', context)


@method_decorator([login_required(redirect_field_name=None, login_url='/account/login'), superuser_required],
                  name='get')
@method_decorator([login_required(redirect_field_name=None, login_url='/account/login'), superuser_required],
                  name='post')
class EditUserView(UpdateView):
    model = Account
    fields = ('first_name', 'last_name', 'username', 'email', 'is_superuser', 'phone_number', 'gender')
    template_name = 'manage_blog/users/edit-user-form.html'

    def get_success_url(self):
        return reverse('admin_users_list')


@method_decorator([login_required(redirect_field_name=None, login_url='/account/login'), superuser_required],
                  name='get')
@method_decorator([login_required(redirect_field_name=None, login_url='/account/login'), superuser_required],
                  name='post')
class CreateUserView(CreateView):
    form_class = UserForm
    template_name = 'manage_blog/users/add-user-form.html'

    def get_success_url(self):
        return reverse('admin_users_list')

    def form_valid(self, form):
        form.instance.set_password(form.cleaned_data['password'])
        return super().form_valid(form)


class BlockUnblockView(View):
    @method_decorator([login_required(redirect_field_name=None, login_url='/account/login'), superuser_required])
    def post(self, request):
        user = Account.objects.get(pk=request.POST['u_id'])
        user.is_active = not user.is_active
        user.save()
        return redirect('admin_users_list')


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
