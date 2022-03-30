from django.urls import path
from . import views

urlpatterns = [
    # posts
    path('submit-edit-post', views.PostEditAdmin.as_view(), name="adminSubmitEditPost"),
    path('delete-post/<p_id>', views.post_delete_admin, name="admin_delete_post"),
    path('add-post', views.AddPostAdmin.as_view(), name="admin_add_post"),
    path('posts', views.PostsAdminView.as_view(), name="admin-posts"),
    path('edit-post/<pk>', views.PostEditAdmin.as_view(), name="admin-edit-post"),
    # users
    path('users', views.AllUsersView.as_view(), name='admin_users_list'),
    path('edit-user/<pk>', views.EditUserView.as_view(), name='admin_edit_user'),
    path('create-user', views.CreateUserView.as_view(), name='admin_create_user'),
    path('block-unblock', views.BlockUnblockView.as_view(), name='admin_block_unblock_user'),
    # Blocked Words
    path('blocked-words', views.AllBlockedWordsView.as_view(), name='admin_blocked_words'),
    path('edit-word/<pk>', views.EditBlockedWordsView.as_view(), name='admin_edit_blocked_word'),
    path('add-word', views.CreateBlockedWordsView.as_view(), name='admin_add_blocked_word'),
    path('delete-word', views.DeleteBlockedWordsView.as_view(), name='admin_delete_blocked_word'),
    # Categories
    path('categories', views.ListCategories.as_view(), name='admin_categories-list'),
    path('add-category', views.CreateCategories.as_view(), name='admin_add_category'),
    path('edit-category/<pk>', views.EditCategories.as_view(), name='admin_edit_category'),
    path('delete-category', views.DeleteCategories.as_view(), name='admin_delete_category'),

]
