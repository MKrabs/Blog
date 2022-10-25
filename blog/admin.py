from django.contrib import admin

# Register your models here.

from .models import Post, Project, Tag

admin.site.register(Post)
admin.site.register(Project)
admin.site.register(Tag)
