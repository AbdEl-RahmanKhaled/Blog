from django.urls import path
from . import views

urlpatterns = [
    path('users', views.AllUsersView.as_view(), name='admin_users_list'),
    path('edit-user/<pk>', views.EditUserView.as_view(), name='admin_edit_user'),
    path('create-user', views.CreateUserView.as_view(), name='admin_create_user'),

]
