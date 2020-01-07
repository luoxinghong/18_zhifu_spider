# -*- coding: utf-8 -*-
import pymysql
import logging
import sys
from .items import Question_Item, first_answer_Item, second_answer_Item
from .middlewares import UrlFilterAndAdd, URLRedisFilter


class ZhifuspiderPipeline(object):
    def __init__(self, settings):
        """
        :summary: 类初始化方法,在这里初始化数据库
        """
        self.username = settings.get('MYSQL_USER')
        self.password = settings.get('MYSQL_PASSWORD')
        self.database = settings.get('MYSQL_DB')
        self.host = settings.get('MYSQL_HOST')
        self.port = settings.get('MYSQL_PORT')
        self.c = settings.get('CHARSET')

        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)

        self.dupefilter = UrlFilterAndAdd()

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            settings=crawler.settings
        )

    def open_spider(self, spider):
        try:
            self.conn = pymysql.connect(
                user=self.username,
                passwd=self.password,
                host=self.host,
                port=self.port,
                database=self.database,
                charset=self.c
            )
            self.logger.info('Connectig to database successfully!')
            self.cur = self.conn.cursor()
        except self.conn.Error as e:
            sys.exit('Failed to connect database.', e)

    def close_spider(self, close_spider):
        self.cur.close()
        self.conn.close()
        self.logger.info('爬取结束，spider已经关闭')

    def process_item(self, item, spider):
        """
        :summary: 先判断item是否已经实例化,如果是,就把数据存储进mysql中
        :param item:
        :param spider:
        :return:
        """

        if isinstance(item, Question_Item):
            self.dupefilter.add_url(item['q_url'])
            try:
                self.cur.execute(
                    'insert into question(q_id,q_title,tags,q_detail,q_create_time,' \
                    'q_attention_num,q_scanner_num,answer_num,best_answer_id,q_url,q_full_name,q_alias_name)' \
                    'values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)',
                    (
                        item['q_id'],
                        item['q_title'],
                        item['tags'],
                        item['q_detail'],
                        item['q_create_time'],
                        item['q_attention_num'],
                        item['q_scanner_num'],
                        item['answer_num'],
                        item['best_answer_id'],
                        item['q_url'],
                        item['q_full_name'],
                        item['q_alias_name'])
                )
                self.cur.connection.commit()
            except self.conn.Error as e:
                self.logger.error(e)
        elif isinstance(item, first_answer_Item):
            try:
                statement = (
                    'insert into answer(q_id,answer_id,answer_detail,' \
                    'create_time,agree_num,comment_num,href_num)' \
                    'values(%s,%s,%s,%s,%s,%s,%s)')
                data = (
                    item['q_id'],
                    item['answer_id'],
                    item['answer_detail'],
                    item['create_time'],
                    item['agree_num'],
                    item['comment_num'],
                    item['href_num'],
                )

                self.cur.execute(
                    statement,
                    data
                )
                self.cur.connection.commit()
            except self.conn.Error as e:
                self.logger.error(e)
        elif isinstance(item, second_answer_Item):
            try:
                statement = (
                    'insert into comment(answer_id,comment_detail,vote_count)values(%s,%s,%s)'
                )
                ac_data = (
                    item['answer_id'],
                    item['comment_detail'],
                    item['vote_count'])
                self.cur.execute(
                    statement,
                    ac_data
                )
                self.cur.connection.commit()
            except self.conn.Error as e:
                self.logger.error(e)