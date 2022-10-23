from django.db import models

from sns.models import Search


# Create your models here.
class LabelModel(models.Model):
    name = models.CharField(max_length=30, unique=True)
    type = models.CharField(max_length=10)
    description = models.CharField(max_length=255, blank=True)


class Tweet(models.Model):
    url = models.CharField(max_length=1024, unique=True)
    date = models.DateTimeField()
    content = models.TextField(blank=True)
    t_id = models.IntegerField(unique=True)
    username = models.CharField(max_length=128)
    replyCount = models.IntegerField()
    retweetCount = models.IntegerField()
    likeCount = models.IntegerField()
    quoteCount = models.IntegerField()
    media = models.JSONField()
    search = models.ForeignKey(Search, on_delete=models.CASCADE)
