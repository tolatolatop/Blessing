#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/10/30 13:26
# @Author  : tolatolatop
# @File    : restful.py
from rest_framework import serializers
from rest_framework.pagination import PageNumberPagination, LimitOffsetPagination

from .models import Tweet


class TweetSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Tweet
        fields = ['url', 'username', 'date', 'content', 'likeCount']


class StandardResultsSetPagination(LimitOffsetPagination):
    pass
