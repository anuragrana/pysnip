# Generated by Django 3.2.5 on 2021-07-11 17:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('snip', '0003_alter_snippetmodel_author'),
    ]

    operations = [
        migrations.AddField(
            model_name='snippetmodel',
            name='author_name',
            field=models.CharField(blank=True, max_length=125, null=True),
        ),
    ]
