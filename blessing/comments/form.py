#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/10/23 20:29
# @Author  : tolatolatop
# @File    : form.py
from django import forms
from .models import Comment, Link, Tweet


class CommentForm(forms.Form):
    name = forms.CharField(max_length=30)
    type = forms.CharField(max_length=10)
    description = forms.CharField(max_length=255)
    link = forms.CharField(max_length=2048)

    def create_comment(self):
        comment = Comment(name=self.name, type=self.type, description=self.description)
        t_ids = [int(i) for i in self.link.split(',')]
        tweets = Tweet.object.filter(pk__in=t_ids)

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
