from django.contrib import admin

# Register your models here.
from .models import (
    SnippetModel
)


class SnippetAdmin(admin.ModelAdmin):
    list_display = ('sid', 'title', 'author', 'created_date')


admin.site.register(SnippetModel, SnippetAdmin)
