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
    cmd = 'snscrape --max-results 120 --jsonl %s' % model.query
    cmd = shlex.split(cmd)
    p = sp.Popen(cmd, shell=False, stdout=sp.PIPE, stderr=sp.PIPE)
    out, err = p.communicate()
    if p.returncode == 0:
        result = [json.loads(line) for line in out.decode().splitlines()]
        return result
    raise RuntimeError(' '.join(cmd), err)


def clean_tweet_data(t):
    t["username"] = t["user"]["username"]
    t['t_id'] = t['id']
    for i in ['id', '_type', 'renderedContent', 'user', 'conversationId', 'lang', 'source', 'sourceUrl', 'sourceLabel',
              'outlinks', 'tcooutlinks', 'retweetedTweet', 'quotedTweet', 'inReplyToTweetId', 'inReplyToUser',
              'mentionedUsers', 'coordinates', 'place', 'hashtags', 'cashtags']:
        del t[i]
    return t


def save_tweet(search_obj, tweet_list):
    res = []
    for t in tweet_list:
        # bad code
        t = clean_tweet_data(t)
        t['search'] = search_obj
        update_id = {
            'url': t['url'],
            't_id': t['t_id']
        }
        del t['t_id']
        del t['url']
        obj = Tweet.objects.update_or_create(defaults=update_id, **t)
        res.append(obj)
    return res
