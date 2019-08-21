# -*- coding: utf-8 -*-
BOT_NAME = 'zhifuSpider'
SPIDER_MODULES = ['zhifuSpider.spiders']
NEWSPIDER_MODULE = 'zhifuSpider.spiders'


import datetime
LOG_LEVEL = "INFO"
to_day = datetime.datetime.now()
log_file_path = "../logs/{}_{}_{}.log".format(to_day.year, to_day.month, to_day.day)
LOG_FILE = log_file_path


DEFAULT_REQUEST_HEADERS = {
    'Host': 'www.zhihu.com',
    'Referer': 'https://www.zhihu.com',
    'Connection': 'keep-alive',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; rv:53.0) Gecko/20100101 Firefox/53.0'
}
ZHIHU_COOKIE = {
    'q_c1': '4bd106c430bc418bbf8a269bed33403b|1563170002000|1557714048000',
    'd_c0': '"ADDpny7Taw-PTvW1Hj6_a9uOdGl-OwpMTbY=|1557714046',
    '_xsrf': '××××××××××××××××××××××',
    'capsion_ticket': '×××××××××××××××××××××××',
    '_zap': '×××××××××××××××××××××××',
    'tgw_l7_route': '×××××××××××××××××××××',
    'z_c0': '××××××××××××××××××××××××××××××××'
}


DOWNLOAD_DELAY = 0
DOWNLOAD_FAIL_ON_DATALOSS = False
CONCURRENT_REQUESTS = 1
CONCURRENT_REQUESTS_PER_DOMAIN = 1
CONCURRENT_REQUESTS_PER_IP = 1
COOKIES_ENABLED = False
DOWNLOAD_TIMEOUT = 60


DOWNLOADER_MIDDLEWARES = {
    'scrapy.extensions.downloadermiddlewares.useragent.UserAgentMiddleware': None,
    'zhifuSpider.middlewares.RandomUserAgentMiddleware': 543,
    'scrapy.contrib.downloadermiddleware.httpproxy.HttpProxyMiddleware': 110,
    'zhifuSpider.middlewares.ProxyMiddleware': 100,
}


MYSQL_HOST = '106.12.8.109'
MYSQL_USER = 'root'
MYSQL_PASSWORD = 'lxh123'
MYSQL_DB = 'zhihu'
CHARSET = 'utf8mb4'
MYSQL_PORT = 3306

REDIS_HOST = 'localhost'
REDIS_PORT = 6379
REDIS_PASSWD = "lxh123"
REDIS_DBNAME = 9
REDIS_KEY = "zhifu_lr"


ITEM_PIPELINES = {
    'zhifuSpider.pipelines.ZhifuspiderPipeline': 601,
}
