from django.contrib import admin
from .models import LabelModel


@admin.register(LabelModel)
class LabelAdmin(admin.ModelAdmin):
    pass
