from django.db import models


# Create your models here.
class LabelModel(models.Model):
    name = models.CharField(max_length=30, unique=True)
    type = models.CharField(max_length=10)
    description = models.CharField(max_length=255, blank=True)
