#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/10/23 20:29
# @Author  : tolatolatop
# @File    : form.py
from ruamel.yaml import YAML
from django import forms
from django.urls import reverse_lazy, reverse

from .models import Comment, Link, Tweet


class CommentForm(forms.Form):
    name = forms.CharField(max_length=30)
    type = forms.CharField(max_length=10)
    description = forms.CharField(max_length=255)
    links = forms.CharField(max_length=2048)

    def create_comment(self):
        name = self.cleaned_data['name']
        comment_type = self.cleaned_data['type']
        description = self.cleaned_data['description']
        links = self.cleaned_data['links']
        comment = Comment(name=name, type=comment_type, description=description)
        t_ids = [int(i) for i in links.split(',')]
        tweets = Tweet.objects.filter(pk__in=t_ids)

        links = []
        for tweet in tweets:
            link = Link(comment=comment, tweet=tweet)
            links.append(link)
        for tweet in tweets:
            tweet.last_comments = comment

        comment.save()
        for link in links:
            link.save()

        for tweet in tweets:
            tweet.save()
        return True


class ReportCommentForm(CommentForm):
    report = forms.IntegerField(widget=forms.HiddenInput(), initial="")

    def get_success_url(self):
        return reverse('report-detail', kwargs={'pk': self.cleaned_data['report']})


class FilterForm(forms.Form):

    def __init__(self, file, *args, **kwargs):
        super().__init__(*args, **kwargs)
        yaml = YAML()
        with open(file, 'r') as f:
            field_list = yaml.load(f)
        for field in field_list:
            field_name = field["name"]
            label = field["label"]
            if field["type"] == "text":
                self.fields[field_name] = forms.CharField(label=label, required=False)
            if field["type"] == "choice":
                choices = field["data"]
                self.fields[field_name] = forms.ChoiceField(label=label, choices=choices)
