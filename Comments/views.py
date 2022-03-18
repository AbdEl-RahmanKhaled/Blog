from django.shortcuts import render, redirect
from .models import Comment, BlockedWord
import re


# Create your views here.


def comment(request):
    if request.method == 'POST':
        content = request.POST['comment']
        blocked_words = list(BlockedWord.objects.all().values_list('word', flat=True))
        regex = re.compile('|'.join(blocked_words), re.IGNORECASE)
        found_words = set(regex.findall(content))
        for word in found_words:
            content = content.replace(word, '*' * len(word))
        c = Comment(post_id=request.POST['p_id'], user=request.user, content=content)
        c.save()

    return redirect('postDetails', p_id=request.POST['p_id'])
