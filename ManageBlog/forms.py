from django.forms import ModelForm
from django import forms
from Accounts.models import Account


class UserForm(ModelForm):
    class Meta:
        model = Account
        fields = (
            'first_name', 'last_name', 'username', 'email', 'password', 'is_superuser', 'is_active', 'phone_number',
            'gender')

        widgets = {
            'password': forms.PasswordInput(),
        }
