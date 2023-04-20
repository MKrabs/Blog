from django.contrib import admin

# Register your models here.

from .domain.entities.like import Like
from .domain.entities.comment import Comment
from .domain.entities.post import Post
from .domain.entities.report import Report
from .domain.entities.tag import Tag
from .domain.entities.profile import Profile

admin.site.register(Profile)
admin.site.register(Post)
admin.site.register(Tag)
admin.site.register(Comment)
admin.site.register(Like)
admin.site.register(Report)
