from django.db import models


class Branch(models.Model):
    name = models.CharField(max_length=48, blank=True, default='')
    path = models.CharField(max_length=128)


class Comment(models.Model):
    type = models.CharField(max_length=10)
    description = models.CharField(max_length=255, blank=True)


class LogData(models.Model):
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
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE)
    last_comment = models.ForeignKey(Comment, on_delete=models.SET_NULL, null=True)

    @property
    def comment_type(self):
        if self.last_comment is not None:
            return self.last_comment.type
        return "待确认"


class Link(models.Model):
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)
    log_data = models.ForeignKey(LogData, on_delete=models.CASCADE)
