from django.shortcuts import render
from Accounts.models import Account
from Helpers.Decorators.auth_decorators import *
from django.views import View
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator


# Create your views here.
# admin views
class AllUsersView(View):
    @method_decorator([login_required, superuser_required])
    def get(self, request):
        context = {
            'users': Account.objects.all()
        }
        return None
