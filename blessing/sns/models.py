from django.db import models
from django.urls import reverse


# Create your models here.


class Search(models.Model):
    name = models.CharField(max_length=48, blank=True)
    query = models.CharField(max_length=255)
    modified = models.DateTimeField(auto_now=True)

    def get_absolute_url(self):
        return reverse('search-detail', kwargs={'pk': self.pk})
