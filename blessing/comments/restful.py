#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/10/30 13:26
# @Author  : tolatolatop
# @File    : restful.py
from collections import OrderedDict

from rest_framework import serializers
from rest_framework.pagination import PageNumberPagination, LimitOffsetPagination
from rest_framework.response import Response

from .models import Tweet


class TweetSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Tweet
        fields = ['id', 'comment_type', 'url', 'username', 'date', 'content']


class StandardResultsSetPagination(LimitOffsetPagination):

    def get_paginated_response(self, data):
        return Response(OrderedDict([
            ('total', self.count),
            ('next', self.get_next_link()),
            ('previous', self.get_previous_link()),
            ('rows', data)
        ]))
