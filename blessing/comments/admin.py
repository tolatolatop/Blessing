from django.contrib import admin
from .models import LabelModel, Tweet, Comment


@admin.register(LabelModel)
class LabelAdmin(admin.ModelAdmin):
    pass


@admin.register(Tweet)
class TweetAdmin(admin.ModelAdmin):
    pass


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    pass
