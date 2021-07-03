from django.db import models
import os
import uuid


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
    # Name of the Author
    author = models.CharField(null=False, blank=True, max_length=250)
    upvotes = models.IntegerField(null=True, default=0)
    python_version = models.CharField(max_length=5, null=False, blank=False, choices=version_choices)
    created_date = models.DateTimeField(null=False, blank=True, auto_now_add=True)
    updated_date = models.DateTimeField(null=False, blank=True, auto_now=True)

    class Meta:
        app_label = "snip"
        db_table = "snip_snippets"

    def __str__(self):
        return str(self.title)
