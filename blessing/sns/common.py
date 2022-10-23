#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/10/23 21:35
# @Author  : tolatolatop
# @File    : common.py
import json
import shlex
import subprocess as sp

from .models import Search
from comments.models import Tweet


def call_snscrape(model: Search):
    cmd = 'snscrape --max-results 20 --jsonl %s' % model.query
    cmd = shlex.split(cmd)
    p = sp.Popen(cmd, shell=False, stdout=sp.PIPE, stderr=sp.PIPE)
    out, err = p.communicate()
    if p.returncode == 0:
        result = [json.loads(line) for line in out.decode().splitlines()]
        return result
    raise RuntimeError(' '.join(cmd), err)


def clean_tweet_data(t):
    for i in ['_type', 'renderedContent', 'user', 'conversationId', 'lang', 'source', 'sourceUrl', 'sourceLabel',
              'outlinks', 'tcooutlinks', 'retweetedTweet', 'quotedTweet', 'inReplyToTweetId', 'inReplyToUser',
              'mentionedUsers', 'coordinates', 'place', 'hashtags', 'cashtags']:
        del t[i]
    return t


def save_tweet(tweet_list):
    res = []
    for t in tweet_list:
        t["username"] = t["user"]["username"]
        # bad code
        t = clean_tweet_data(t)
        obj = Tweet(**t)
        obj.save()
        res.append(obj)
    return res
