# Generated by Django 3.2.5 on 2021-07-12 18:22

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('snip', '0005_upvotemodel'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='upvotemodel',
            unique_together={('user', 'snippet')},
        ),
    ]