#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/10/30 13:26
# @Author  : tolatolatop
# @File    : restful.py
from rest_framework import serializers
from rest_framework.pagination import PageNumberPagination

from .models import Tweet


class TweetSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Tweet
        fields = ['url', 'username', 'date', 'content', 'likeCount']


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 100
    page_size_query_param = 'page_size'
    max_page_size = 1000
