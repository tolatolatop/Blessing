#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/10/30 13:26
# @Author  : tolatolatop
# @File    : restful.py
from .models import Tweet
from rest_framework import serializers


class TweetSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Tweet
        fields = ['url', 'username', 'date', 'content', 'likeCount']
