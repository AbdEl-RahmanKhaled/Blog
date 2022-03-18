from django.contrib import admin
from .models import Comment, BlockedWord

# Register your models here.


admin.site.register(Comment)
admin.site.register(BlockedWord)
