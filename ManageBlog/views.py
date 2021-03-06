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
from Comments.models import BlockedWord
from Posts.models import Category


# users
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


# >>>>>>>>>>>>>>>>> Blocked Words <<<<<<<<<<<<<<<<<<<<<<<<

class AllBlockedWordsView(View):
    @method_decorator([login_required(redirect_field_name=None, login_url='/account/login'), superuser_required])
    def get(self, request):
        f_words = BlockedWord.objects.all().order_by('word')
        paginator = Paginator(f_words, 5)
        page = request.GET.get('page')
        page_words = paginator.get_page(page)
        context = {
            'words': page_words
        }
        return render(request, 'manage_blog/blocked_words/blocked-words-list.html', context)


@method_decorator([login_required(redirect_field_name=None, login_url='/account/login'), superuser_required],
                  name='get')
@method_decorator([login_required(redirect_field_name=None, login_url='/account/login'), superuser_required],
                  name='post')
class EditBlockedWordsView(UpdateView):
    model = BlockedWord
    fields = ('word',)
    template_name = 'manage_blog/blocked_words/blocked-words-form.html'

    def get_success_url(self):
        return reverse('admin_blocked_words')


@method_decorator([login_required(redirect_field_name=None, login_url='/account/login'), superuser_required],
                  name='get')
@method_decorator([login_required(redirect_field_name=None, login_url='/account/login'), superuser_required],
                  name='post')
class CreateBlockedWordsView(CreateView):
    model = BlockedWord
    fields = ('word',)
    template_name = 'manage_blog/blocked_words/blocked-words-form.html'

    def get_success_url(self):
        return reverse('admin_blocked_words')


class DeleteBlockedWordsView(View):
    @method_decorator([login_required(redirect_field_name=None, login_url='/account/login'), superuser_required])
    def post(self, request):
        word = BlockedWord.objects.get(pk=request.POST['w_id'])
        word.delete()
        return redirect('admin_blocked_words')


# >>>>>>>>>>>>>>>>>>>>>>> POST >>>>>>>>>>>>>>>>>>
class PostsAdminView(View):
    # template = 'posts/admin-posts.html'

    def get(self, request):
        posts = Post.objects.all()
        paginator = Paginator(posts, 5)
        page = request.GET.get('page')
        page_posts = paginator.get_page(page)
        context = {
            'posts': page_posts
        }
        return render(request, 'manage_blog/posts/admin-posts.html', context)


class PostEditAdmin(UpdateView):
    model = Post
    fields = ('title', 'category', 'content', 'pic')
    template_name = 'manage_blog/posts/adminEditPost.html'

    def get_success_url(self):
        return reverse('admin-posts')


class AddPostAdmin(CreateView):
    model = Post
    fields = ('title', 'category', 'content', 'pic')
    template_name = 'manage_blog/posts/adminAddPost.html'

    def get_success_url(self):
        return reverse('admin-posts')


def post_delete_admin(request, p_id):
    post = Post.objects.get(id=p_id)
    post.delete()
    return redirect('admin-posts')


# >>>>>>>>>>>>>>>>>>>>>>> Categories >>>>>>>>>>>>>>>>>>

class ListCategories(View):
    @method_decorator([login_required(redirect_field_name=None, login_url='/account/login'), superuser_required])
    def get(self, request):
        category = Category.objects.exclude(id="6")
        paginator = Paginator(category, 5)
        page = request.GET.get('page')
        page_category = paginator.get_page(page)
        context = {
            'categories': page_category
        }
        return render(request, 'manage_blog/category/category-list.html', context)


@method_decorator([login_required(redirect_field_name=None, login_url='/account/login'), superuser_required],
                  name='get')
@method_decorator([login_required(redirect_field_name=None, login_url='/account/login'), superuser_required],
                  name='post')
class CreateCategories(CreateView):
    model = Category
    fields = ('category',)
    template_name = 'manage_blog/category/categories-form.html'

    def get_success_url(self):
        return reverse('admin_categories-list')


@method_decorator([login_required(redirect_field_name=None, login_url='/account/login'), superuser_required],
                  name='get')
@method_decorator([login_required(redirect_field_name=None, login_url='/account/login'), superuser_required],
                  name='post')
class EditCategories(UpdateView):
    model = Category
    fields = ('category',)
    template_name = 'manage_blog/category/categories-form.html'

    def get_success_url(self):
        return reverse('admin_categories-list')


class DeleteCategories(View):
    @method_decorator([login_required(redirect_field_name=None, login_url='/account/login'), superuser_required])
    def post(self, request):
        category = Category.objects.get(pk=request.POST['cat_id'])
        category.delete()
        return redirect('admin_categories-list')
