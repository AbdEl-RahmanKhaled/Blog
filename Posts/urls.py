from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('timeline', views.posts, name ='Posts'),
    path('Post_detail/<p_id>', views.post_detail, name='postDetails'),
    path('Likes', views.like, name ="like"),
    path('dislikes', views.dislikes, name ="dislikes")
]
