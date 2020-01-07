#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@author: 罗兴红
@contact: EX-LUOXINGHONG001@pingan.com.cn
@file: utils.py
@time: 2019/8/5 11:19
@desc:
'''
import json
import requests
import logging
import random


logger = logging.getLogger(__name__)


def get_one_proxy():
    """ 使用API接口获取一个代理IP"""
    # API接口
    orderid = '927741088534585'
    api_url = "http://dps.kdlapi.com/api/getdps/?orderid=927741088534585&num=1&pt=1&format=json&sep=1"
    # API接口返回的IP
    r = requests.get(api_url)
    if r.status_code != 200:
        logger.error("fail to get proxy")
        return None
    ip_list = r.json()['data']['proxy_list']
    return random.choice(ip_list)


if __name__ == '__main__':
    print("proxy: ", get_one_proxy())
