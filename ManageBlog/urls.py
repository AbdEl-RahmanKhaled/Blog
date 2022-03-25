from django.urls import path
from . import views

urlpatterns = [
    # posts
    path('submit-edit-post', views.PostEditAdmin.as_view(), name="adminSubmitEditPost"),
    path('delete-post/<p_id>', views.PostDeleteAdmin, name="adminDeletePost"),
    path('add-post', views.AddPostAdmin, name="adminAddPost"),
    path('posts', views.PostsAdminView.as_view(), name="admin-posts"),
    path('edit-post/<p_id>', views.PostEditAdmin.as_view(), name="adminEditPost"),
    # users
    path('users', views.AllUsersView.as_view(), name='admin_users_list'),
    path('edit-user/<pk>', views.EditUserView.as_view(), name='admin_edit_user'),
    path('create-user', views.CreateUserView.as_view(), name='admin_create_user'),
    path('block-unblock', views.BlockUnblockView.as_view(), name='admin_block_unblock_user'),

]
