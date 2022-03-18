from django.db import models
import Accounts.models
import Posts.models
import Posts.models


# Create your models here.


class Comments(models.Model):
    post = models.ForeignKey(Posts.models.Post, on_delete=models.CASCADE, related_name='Comments')
    user = models.ForeignKey(Accounts.models.Account, on_delete=models.CASCADE, default='Unknown',
                             related_name='Comment Owner')
    content = models.TextField(verbose_name='Comment Content')
    created_on = models.DateTimeField(auto_now_add=True, verbose_name='Comment Time')
