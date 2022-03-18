from django.db import models


class Category(models.Model):
    category = models.CharField(max_length=30, blank=False, null=False, verbose_name='Category')


class Post(models.Model):
    title = models.CharField(max_length=100, blank=False, verbose_name='Title')
    pic = models.ImageField(upload_to='photos/%Y/%M/%D', verbose_name='Post Picture')
    content = models.CharField(max_length=200, blank=False, verbose_name='Post Content')
    category = models.ForeignKey(Category, on_delete=models.SET_DEFAULT, default='undefined',
                                 related_name='posts_related')
    likes = models.IntegerField(default=0)
    dislikes = models.IntegerField(default=0)
