from django.contrib import admin

from api.models import Post, Comment, Follow

admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(Follow)
