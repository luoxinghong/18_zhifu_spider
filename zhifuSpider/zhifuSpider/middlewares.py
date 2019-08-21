# -*- coding: utf-8 -*-
import random
from scrapy.downloadermiddlewares.useragent import UserAgentMiddleware
from scrapy.dupefilters import RFPDupeFilter
from scrapy.utils.url import canonicalize_url
from . import settings
import hashlib
import redis
from fake_useragent import UserAgent
import os
from scrapy import signals
import scrapy
import base64
import logging


class RandomUserAgentMiddleware(object):
    def __init__(self, crawler):
        super(RandomUserAgentMiddleware, self).__init__()
        self.ua = UserAgent()
        # 从setting文件中读取RANDOM_UA_TYPE值
        self.ua_type = crawler.settings.get('RANDOM_UA_TYPE', 'random')


    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler)

    def process_request(self, request, spider):
        def get_ua():
            '''Gets random UA based on the type setting (random, firefox…)'''
            return getattr(self.ua, self.ua_type)

        user_agent_random = get_ua()
        request.headers.setdefault('User-Agent', user_agent_random)


class URLRedisFilter(RFPDupeFilter):
    """ 只根据url去重"""

    def __init__(self, path=None, debug=False):
        RFPDupeFilter.__init__(self, path)
        self.dupefilter = UrlFilterAndAdd()

    def request_seen(self, request):
        # 校验，新增2行代码
        if self.dupefilter.check_url(request.url):
            return True

        # 保留中间页面的去重规则不变，不然爬虫在运行过程中容易出现死循环
        fp = self.request_fingerprint(request)
        if fp in self.fingerprints:
            return True
        self.fingerprints.add(fp)
        if self.file:
            self.file.write(fp + os.linesep)


class UrlFilterAndAdd(object):
    def spider_opened(self, spider):
        return spider.name

    def __init__(self):
        redis_config = {
            "host": settings.REDIS_HOST,  # redis ip
            "port": settings.REDIS_PORT,
            "password": settings.REDIS_PASSWD,
            "db": settings.REDIS_DBNAME,
        }

        pool = redis.ConnectionPool(**redis_config)
        self.pool = pool
        self.redis = redis.StrictRedis(connection_pool=pool)
        self.key = settings.REDIS_KEY

    def url_sha1(self, url):
        fp = hashlib.sha1()
        # 对url中的构成数据进行了重新排列，例如有些url中请求参数一样，但是顺序不同
        fp.update(canonicalize_url(url).encode("utf-8"))
        url_sha1 = fp.hexdigest()
        return url_sha1

    def check_url(self, url):
        # sha1 = self.url_sha1(url)
        # 此处只判断url是否在set中，并不添加url信息，
        # 防止将起始url 、中间url(比如列表页的url地址)写入缓存中
        isExist = self.redis.sismember(self.key, url)
        return isExist

    def add_url(self, url):
        # sha1 = self.url_sha1(url)
        # 将经过hash的url添加到reids的集合中，key为spider_redis_key，命令为SMEMBERS spider_redis_key
        added = self.redis.sadd(self.key, url)
        return added


from .utils import fetch_one_proxy
username = "767166726"
password = "lnawbqlr"
proxy = fetch_one_proxy()  # 获取一个代理
logger = logging.getLogger(__name__)
THRESHOLD = 3  # 换ip阈值
fail_time = 0  # 此ip异常次数
# 代理中间件
class ProxyMiddleware(object):
    def process_request(self, request, spider):
        proxy_url = 'http://%s:%s@%s' % (username, password, proxy)
        request.meta['proxy'] = proxy_url
        logger.debug("using proxy: {}".format(request.meta['proxy']))
        logger.debug("fail_time: {}".format(fail_time))
        auth = "Basic %s" % (base64.b64encode(('%s:%s' % (username, password)).encode('utf-8'))).decode('utf-8')
        request.headers['Proxy-Authorization'] = auth


    def process_response(self, request, response, spider):
        global fail_time, proxy, THRESHOLD
        if not(200 <= response.status < 300):
            fail_time += 1
            if fail_time >= THRESHOLD:
                proxy = fetch_one_proxy()
                fail_time = 0
        return response
