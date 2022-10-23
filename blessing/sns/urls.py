#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/10/23 20:47
# @Author  : tolatolatop
# @File    : urls.py
from django.urls import path

from .views import SearchDetailView, SearchCreateView

urlpatterns = [
    path('search', SearchCreateView.as_view(), name='search'),
    path('search/<int:pk>', SearchDetailView.as_view(), name='search-detail'),
]
