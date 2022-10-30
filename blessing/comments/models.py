import pathlib

from django.db import models
import pandas as pd
from django.conf import settings


def load_excel_local(branch, file_path: pathlib.Path):
    df = pd.read_excel(file_path, index_col=0)
    data_list = [{k: v for k, v in m.items() if pd.notnull(v)} for m in df.to_dict(orient='rows')]
    for data in data_list:
        data['branch'] = branch
        LogData.objects.update_or_create(defaults=data, url=data["url"])
    return True


class Branch(models.Model):
    name = models.CharField(max_length=48, blank=True, default='')
    path = models.CharField(max_length=128)

    def save(self, *args, **kwargs):
        file: pathlib.Path = settings.DATA_DIR / self.path
        res = super(Branch, self).save(*args, **kwargs)
        load_excel_local(self, file)
        return res


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
