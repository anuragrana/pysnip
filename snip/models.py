from django.db import models
import os
import uuid
from django.conf import settings


def upload_path(instance, filename):
    extension = filename.split('.')[-1]
    filename = uuid.uuid1().hex + "." + extension;
    return os.path.join("uploads", "code_images", filename)


class SnippetModel(models.Model):

    version_choices = (
        ('2.7', '2.7'),
        ('3.0', '3.0'),
        ('3.3', '3.3'),
        ('3.4', '3.4'),
        ('3.5', '3.5'),
        ('3.6', '3.6'),
        ('3.7', '3.7'),
        ('3.8', '3.8'),
        ('3.9', '3.9'),
    )

    sid = models.AutoField(primary_key=True, null=False, blank=True)
    title = models.CharField(max_length=125, null=False, blank=False)
    description = models.CharField(null=True, blank=True, max_length=1024)
    code = models.TextField(null=False, blank=False)
    image = models.ImageField(upload_to=upload_path, null=True, blank=True, max_length=1000)
    # User Id from Auth User table
    author = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.DO_NOTHING)
    # Author name - String - Can be set by Admin to override author or when copying snippet from Internet
    author_name = models.CharField(null=True, blank=True, max_length=125)
    upvotes = models.IntegerField(null=True, default=0)
    python_version = models.CharField(max_length=5, null=False, blank=False, choices=version_choices)
    created_date = models.DateTimeField(null=False, blank=True, auto_now_add=True)
    updated_date = models.DateTimeField(null=False, blank=True, auto_now=True)

    class Meta:
        app_label = "snip"
        db_table = "snip_snippets"

    def __str__(self):
        return str(self.title)

    def get_author(self):
        author = ''

        if self.author_name:
            return self.author_name

        if self.author.first_name:
            author = self.author.first_name
        if author and self.author.last_name:
            author = author + " " + self.author.last_name

        if not author:
            author = self.author.username

        return author
