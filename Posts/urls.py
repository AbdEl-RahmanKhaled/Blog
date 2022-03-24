from django.urls import path
from . import views

urlpatterns = [
    path('', views.posts, name ='index'),
    path('posts/Post_detail/<p_id>', views.post_detail, name='postDetails'),
    path('posts/Likes', views.like, name ="like"),
    path('posts/dislikes', views.dislikes, name ="dislikes"),
    path('posts/sub_category/<cat_id>', views.sub_category, name="sub_category"),
    path('posts/unsub_category/<cat_id>', views.unsub_category, name="unsub_category"),
    path('posts/admin-posts', views.PostsAdminView.as_view(), name="admin-posts"),
    path('posts/admin-editPost/<p_id>', views.PostEditAdmin.as_view(), name="adminEditPost"),
    path('posts/admin-deletePost/<p_id>', views.PostDeleteAdmin, name="adminDeletePost")
]
