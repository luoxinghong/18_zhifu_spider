#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@author: 罗兴红
@contact: EX-LUOXINGHONG001@pingan.com.cn
@file: test.py
@time: 2019/8/5 13:41
@desc:
'''
import datetime
import redis

r = redis.Redis(host='106.12.8.109', password='lxh123', port=6379, db=9)

f = open("./urls.txt", "r", encoding="utf-8").readlines()

f = [i.strip() for i in f]

for url in f:
    r.sadd("zhihu", "{}".format(url))
