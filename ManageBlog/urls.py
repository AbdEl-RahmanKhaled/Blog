from django.urls import path
from . import views

urlpatterns = [
    path('submit-edit-post', views.PostEditAdmin.as_view(), name="adminSubmitEditPost"),
    path('delete-post/<p_id>', views.PostDeleteAdmin, name="adminDeletePost"),
    path('add-post', views.AddPostAdmin, name="adminAddPost"),
    path('posts', views.PostsAdminView.as_view(), name="admin-posts"),
    path('edit-post/<p_id>', views.PostEditAdmin.as_view(), name="adminEditPost")
]
