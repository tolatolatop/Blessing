from django.contrib import admin
from .models import LogData, Comment, Branch


@admin.register(LogData)
class LogDataAdmin(admin.ModelAdmin):
    pass


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    pass


@admin.register(Branch)
class UpstreamAdmin(admin.ModelAdmin):
    pass
