from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.forms import UserCreationForm
from Accounts.models import Account
from Helpers.Decorators.auth_decorators import *
from django.views import View
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from .forms import UserForm
from django.views.generic import UpdateView, CreateView


# Create your views here.
# admin views
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
