import datetime
from django.shortcuts import render, HttpResponseRedirect, reverse, redirect
from django.views import View
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from .Handlers.views_account_handler import ViewsAccountHandler
from django.contrib import messages, auth
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode
from .utils import token_generator, PasswordResetTokenGenerator
from .models import Account
from Helpers.Decorators.auth_decorators import *


class RegisterView(View):
    template = 'accounts/register.html'

    @method_decorator(logout_required)
    def get(self, request):
        return render(request, self.template)

    @method_decorator(logout_required)
    def post(self, request):
        context = {
            'data': request.POST,
        }
        vah = ViewsAccountHandler(request=request)
        vah.first_name = request.POST.get('first_name')
        vah.last_name = request.POST.get('last_name')
        vah.username = request.POST.get('username')
        vah.email = request.POST.get('email')
        vah.password = request.POST.get('password')
        vah.set_phone(request.POST.get('phone_number'))
        vah.gender = request.POST.get('gender')
        created, errors = vah.register()

        if created:
            messages.success(request,
                             'Your account has been registered successfully'
                             ', check your email inbox for activation instructions')
            return redirect('login')
        else:
            for error in errors:
                messages.add_message(request, messages.ERROR, error)
        return render(request, self.template, context)


class LoginView(View):
    template_name = 'accounts/login.html'

    @method_decorator(logout_required)
    def get(self, request):
        return render(request, self.template_name)

    @method_decorator(logout_required)
    def post(self, request):
        context = {
            'data': request.POST
        }
        username = request.POST.get('username')
        password = request.POST.get('password')
        if '@' in username:
            kwargs = {'email': username, 'password': password}
        else:
            kwargs = {'username': username, 'password': password}
        acc = auth.authenticate(**kwargs)
        if acc is not None:
            auth.login(request, acc)
            return redirect('/')

        messages.error(request, 'username or password not correct')
        return render(request, self.template_name, context)


@login_required(redirect_field_name=None, login_url='/accounts/login')
def logout(request):
    # if request.method == 'POST':
    auth.logout(request)
    messages.success(request, 'You are now logged out')
    return redirect('login')


class ActivateAccountView(View):
    def get(self, request, uidb64, token):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = Account.objects.get(pk=uid)
        except Exception as e:
            user = None

        if user is not None and token_generator.check_token(user, token):
            user.is_verified_email = True
            user.save()
            messages.add_message(request, messages.SUCCESS,
                                 'account activated successfully')
        messages.error(request, 'Not Valid Request')
        return redirect('login')


class RequestResetPasswordView(View):
    template = 'accounts/request-reset-password.html'

    @method_decorator(logout_required)
    def get(self, request):
        return render(request, self.template)

    @method_decorator(logout_required)
    def post(self, request):
        context = {
            'data': request.POST,
        }
        vah = ViewsAccountHandler(request=request, email=request.POST.get('email'))
        done = vah.request_rest_password()

        if done:
            messages.success(request, 'The email has been sent by instructions to rest your password')
            return redirect('login')
        messages.error(request, 'Email dose not exist you can register new account with this email')
        return render(request, self.template, context)


class RestPasswordView(View):
    template = 'accounts/set-new-password.html'

    def get(self, request, uidb64, token):
        account, is_valid_token = self.decode_user(uidb64, token)

        if is_valid_token and account is not None:
            return render(request, self.template)
        else:
            messages.error(request, 'Password reset link, is invalid, please request a new one')
            return redirect('request-rest-password')

    def post(self, request, uidb64, token):
        account, is_valid_token = self.decode_user(uidb64, token)
        if account is not None and is_valid_token:
            vah = ViewsAccountHandler(request=request, account_obj=account, password=request.POST.get('password'))
            valid_password = vah.change_password()

            if valid_password:
                messages.success(request, 'your password has been changed you can use new password to login')
                return redirect('login')
            messages.error(request, 'your new password is not valid please use more than 6 characters')
            return render(request, self.template)
        else:
            messages.error(request, 'Not Valid Request')
            return redirect('login')

    @staticmethod
    def decode_user(uidb64, token):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            account = Account.objects.get(pk=uid)
        except Exception as e:
            account = None

        return account, PasswordResetTokenGenerator().check_token(account, token)


class ActivationRequiredView(View):
    @method_decorator([login_required, not_verified_acc_only])
    def get(self, request):
        return render(request, 'accounts/activation-required.html')

    @method_decorator([login_required, not_verified_acc_only])
    def post(self, request):
        vah = ViewsAccountHandler(request=request, account_obj=request.user)
        vah.send_email_verification()
        messages.success(request, 'Email verification has been sent, check your mailbox and follow the instructions')
        return render(request, 'accounts/activation-required.html')
