# Generated by Django 4.0.3 on 2022-03-19 14:39

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('Posts', '0004_postlikes_postdislikes'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='subbed_users',
            field=models.ManyToManyField(related_name='users', to=settings.AUTH_USER_MODEL),
        ),
    ]