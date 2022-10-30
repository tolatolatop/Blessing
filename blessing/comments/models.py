from django.db import models

from sns.models import Search


# Create your models here.
class LabelModel(models.Model):
    name = models.CharField(max_length=30, unique=True)
    type = models.CharField(max_length=10)
    description = models.CharField(max_length=255, blank=True)


class Comment(models.Model):
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
    media = models.JSONField(null=True)
    search = models.ForeignKey(Search, on_delete=models.CASCADE)
    last_comments = models.ForeignKey(Comment, on_delete=models.SET_NULL, null=True)

    @property
    def comment_type(self):
        if self.last_comments is not None:
            return self.last_comments.type
        return ""


class Link(models.Model):
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)
    tweet = models.ForeignKey(Tweet, on_delete=models.CASCADE)


class Report(models.Model):
    search = models.ForeignKey(Search, on_delete=models.CASCADE)
