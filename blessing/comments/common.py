#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/10/24 5:47
# @Author  : tolatolatop
# @File    : common.py

import io
import json
from typing import List

import xlsxwriter
from django.http import FileResponse
from django.conf import settings

from .models import Tweet, Report


def read_headers(file_path):
    data_dir = settings.STATIC_DIR
    json_file = data_dir / file_path
    with json_file.open('r') as f:
        data = json.load(f)
    data = dict((i['field'], i['title']) for i in data)
    return data


def export_excel(request, report_id):
    report_obj = Report.objects.filter(pk=report_id).first()
    saved_filter = request.session.get("saved_filter", {})
    tweets = Tweet.objects.filter(search=report_obj.search, **saved_filter)
    buffer = create_report("tweet_info.json", tweets)
    return FileResponse(buffer, as_attachment=True, filename='report.xlsx')


def create_report(header_file, data):
    buffer = io.BytesIO()
    workbook = xlsxwriter.Workbook(buffer)
    worksheet = workbook.add_worksheet()
    headers = read_headers(header_file)
    len_headers = len(headers)
    for col, h in enumerate(headers):
        worksheet.write(0, col, h)

    for row, t in enumerate(data, start=1):
        for col, h in enumerate(headers):
            worksheet.write(row, col, str(getattr(t, h)))
        if t.last_comments is not None:
            worksheet.write(row, len_headers, t.last_comments.description)
    workbook.close()
    buffer.seek(0)

    return buffer
