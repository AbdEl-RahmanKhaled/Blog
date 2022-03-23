from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('posts/timeline', views.posts, name='posts'),
    path('posts/Post-detail/<p_id>', views.post_detail, name='postDetails'),
    path('posts/Likes', views.like, name="like"),
    path('posts/dislikes', views.dislikes, name="dislikes"),
    path('posts/sub-category/<cat_id>', views.sub_category, name="sub_category"),
    path('posts/unsub-category/<cat_id>', views.unsub_category, name="unsub_category"),
]
