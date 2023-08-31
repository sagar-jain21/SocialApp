from django.contrib import admin

from .models import Post, Like, Comment, Follow


# Register your models here.
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ["uuid", "user", "title", "content"]


@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = ["uuid", "user", "post"]


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ["uuid", "user", "post", "comment"]


@admin.register(Follow)
class FollowAdmin(admin.ModelAdmin):
    list_display = ["uuid", "user", "user_following"]
