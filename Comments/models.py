from django.db import models
from Accounts.models import Account
from Posts.models import Post


# Create your models here.


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='Comments')
    user = models.ForeignKey(Account, on_delete=models.CASCADE, default='Unknown',
                             related_name='comment_owner')
    content = models.TextField(verbose_name='Comment Content')
    created_on = models.DateTimeField(auto_now_add=True, verbose_name='Comment Time')

    def __str__(self):
        return self.post.title


class BlockedWord(models.Model):
    word = models.CharField(max_length=50, null=False, blank=False)

    def __str__(self):
        return self.word
