#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/10/23 20:29
# @Author  : tolatolatop
# @File    : form.py
from ruamel.yaml import YAML
from django import forms
from django.conf import settings

from .models import Comment, Link, LogData


class CommentForm(forms.Form):
    type = forms.CharField(max_length=10)
    description = forms.CharField(max_length=255)
    links = forms.CharField(max_length=2048)

    def create_comment(self):
        comment_type = self.cleaned_data['type']
        description = self.cleaned_data['description']
        links = self.cleaned_data['links']
        comment = Comment(type=comment_type, description=description)
        t_ids = [int(i) for i in links.split(',')]
        log_data_collect = LogData.objects.filter(pk__in=t_ids)

        links = []
        for log_data in log_data_collect:
            link = Link(comment=comment, log_data=log_data)
            links.append(link)
        for log_data in log_data_collect:
            log_data.last_comment = comment

        comment.save()
        for link in links:
            link.save()

        for log_data in log_data_collect:
            log_data.save()
        return True


class YamlForm(forms.Form):

    def __init__(self, file, init_value: dict, *args, **kwargs):
        super().__init__(*args, **kwargs)
        yaml = YAML()
        with open(file, 'r') as f:
            field_list = yaml.load(f)
        for field in field_list:
            field_name = field["name"]
            label = field["label"]
            if field["type"] == "text":
                field_obj = forms.CharField(label=label, required=False)
                field_obj.initial = init_value.get(field_name, "")
            elif field["type"] == "choice":
                choices = field["data"]
                field_obj = forms.ChoiceField(label=label, choices=choices)
                field_obj.initial = init_value.get(field_name, "")
            else:
                field_obj = None
            self.fields[field_name] = field_obj


class FilterForm(YamlForm):
    yaml_path = settings.STATIC_DIR / "log_data_filter.yaml"

    def __init__(self, init_value: dict, *args, **kwargs):
        super(FilterForm, self).__init__(self.yaml_path, init_value, *args, **kwargs)


class TimelineCommentForm(YamlForm):
    yaml_path = settings.STATIC_DIR / "comment.yaml"

    def __init__(self, *args, **kwargs):
        super(TimelineCommentForm, self).__init__(self.yaml_path, {}, *args, **kwargs)
