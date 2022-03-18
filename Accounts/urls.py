from django.urls import path
from .views import *

urlpatterns = [ 
    path('login', LoginView.as_view(), name='login'),
    path('register', RegisterView.as_view(), name='register'),
    path('logout', logout, name='logout'),
    path('request-rest-password', RequestResetPasswordView.as_view(), name='request-rest-password'),
    path('activation-required', ActivationRequiredView.as_view(), name='activation-required'),
    path('activate/<uidb64>/<token>', ActivateAccountView.as_view(), name='activate'),
    path('set-new-password/<uidb64>/<token>', RestPasswordView.as_view(), name='set-new-password'),
]
