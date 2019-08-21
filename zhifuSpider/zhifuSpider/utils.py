#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@author: 罗兴红
@contact: EX-LUOXINGHONG001@pingan.com.cn
@file: utils.py
@time: 2019/8/5 11:19
@desc:
'''
import requests
import json
import logging

orderid = '926497502079573'
api_url = "https://dps.kdlapi.com/api/getdps/?orderid={}&num=10&signature=lm37dlk419eviyd5vhlbg4bxozyqita1&pt=1&format=json&sep=1"

logger = logging.getLogger(__name__)

def fetch_one_proxy():
    fetch_url = api_url.format(orderid)
    r = requests.get(fetch_url)
    if r.status_code != 200:
        logger.error("fail to fetch proxy")
        return False
    content = json.loads(r.content.decode('utf-8'))
    ips = content['data']['proxy_list']
    return ips[0]

if __name__ == '__main__':
    print("proxy: ", fetch_one_proxy())