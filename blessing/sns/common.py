#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/10/23 21:35
# @Author  : tolatolatop
# @File    : common.py
import json
import shlex
import subprocess as sp
from datetime import datetime

import pandas as pd
from django.conf import settings

from .models import Search
from comments.models import LogData


def call_snscrape(model: Search):
    cmd = 'snscrape --max-results 120 --jsonl %s' % model.query
    cmd = shlex.split(cmd)
    p = sp.Popen(cmd, shell=False, stdout=sp.PIPE, stderr=sp.PIPE)
    out, err = p.communicate()
    if p.returncode == 0:
        result = [json.loads(line) for line in out.decode().splitlines()]
        return result
    raise RuntimeError(' '.join(cmd), err)


def clean_log_data(t):
    t["username"] = t["user"]["username"]
    t['t_id'] = t['id']
    for i in ['id', '_type', 'renderedContent', 'user', 'conversationId', 'lang', 'source', 'sourceUrl', 'sourceLabel',
              'outlinks', 'tcooutlinks', 'retweetedTweet', 'quotedTweet', 'inReplyToTweetId', 'inReplyToUser',
              'mentionedUsers', 'coordinates', 'place', 'hashtags', 'cashtags']:
        del t[i]
    return t


def save_log_data_as_excel(log_data_collect):

    log_data_collect = [clean_log_data(d) for d in log_data_collect]
    df = pd.DataFrame(log_data_collect)

    timestamp = datetime.now().strftime("%Y%m%d%H%M%f")
    file_path = settings.DATA_DIR / f"{timestamp}.xlsx"
    df.to_excel(file_path)
    return True


def save_log_data(search_obj, log_data_collect):
    res = []
    for t in log_data_collect:
        # bad code
        t = clean_log_data(t)
        t['search'] = search_obj
        update_id = {
            'url': t['url'],
            't_id': t['t_id']
        }
        obj = LogData.objects.update_or_create(defaults=t, **update_id)
        res.append(obj)
    return res
