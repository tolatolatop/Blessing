import datetime

from django.db import models
from django.urls import reverse


# Create your models here.


class Search(models.Model):
    name = models.CharField(max_length=48, blank=True, default='')
    query = models.CharField(max_length=255, default='')
    modified = models.DateTimeField(auto_now=True)

    def get_absolute_url(self):
        return reverse('search-detail', kwargs={'pk': self.pk})
