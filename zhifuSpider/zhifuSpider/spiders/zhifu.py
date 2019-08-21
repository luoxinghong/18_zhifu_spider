# -*- coding: utf-8 -*-
from ..settings import *
import pymysql
import scrapy
import json
import time
from bs4 import BeautifulSoup
from scrapy.http import Request
from scrapy.selector import Selector
from ..items import Question_Item, answer_Item, answer_comment_Item, author_seeds_Item
import re
import sys
import io


class ZhihuSpider(scrapy.Spider):
    name = 'zhifu'
    allowed_domain = ['zhihu.com']
    start_url = ['https://www.zhihu.com/']
    answer_url = 'https://www.zhihu.com/api/v4/questions/{ques_id}/answers?include=' \
                 'data[*].is_normal,admin_closed_comment,reward_info,is_collapsed,annotatio' \
                 'n_action,annotation_detail,collapse_reason,is_sticky,collapsed_by,suggest_e' \
                 'dit,comment_count,can_comment,content,editable_content,voteup_count,reshipment' \
                 '_settings,comment_permission,created_time,updated_time,review_info,relevant_info,' \
                 'question,excerpt,relationship.is_authorized,is_author,voting,is_thanked,is_nothelp;' \
                 'data[*].mark_infos[*].url;data[*].author.follower_count,badge[?(type=best_answerer)].' \
                 'topics;dci_info&limit=10&offset={offset}&sort_by=default'
    comm_url = 'https://www.zhihu.com/api/v4/answers/{answer_id}/comments?include=data' \
               '[*].author,collapsed,reply_to_author,disliked,content,voting,vote_count,' \
               'is_parent_author,is_author&order=normal&limit=20&offset={offset}&status=' \
               'open'
    url1 = 'https://www.zhihu.com/api/v4/search_v3?t=general&q={}&correction=1&offset={}&limit=10'

    def __init__(self, *args, **kwargs):
        super(ZhihuSpider, self).__init__(*args, **kwargs)
        self.base_url = 'https://www.zhihu.com'

    def change_time(self, time_str):
        timeArray = time.localtime(time_str)
        otherstyle_time = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
        return otherstyle_time

    def start_requests(self):
        try:
            self.conn = pymysql.connect(
                user=MYSQL_USER,
                passwd=MYSQL_PASSWORD,
                host=MYSQL_HOST,
                port=MYSQL_PORT,
                database=MYSQL_DB,
                charset=CHARSET)
            self.logger.info('Spider connectig to database successfully!')
            self.cur = self.conn.cursor()
        except self.conn.Error as e:
            print('Spider Failed to connect database.')
            sys.exit()
        try:
            self.cur.execute('SELECT key_word FROM zhihu.key_words where is_crawled=0 limit 1')
        except Exception as e:
            print('the key_word is crawled,try to add new')
            sys.exit()
        alldata = self.cur.fetchall()

        for rec in alldata:
            for i in range(0, 500, 10):
                yield Request(
                    url=self.url1.format(rec[0], i),
                    method='GET',
                    cookies=ZHIHU_COOKIE,
                    dont_filter=True,
                    meta={'topic': rec[0]})

    def parse(self, response):
        topic = response.meta['topic']
        json_body = json.loads(response.body_as_unicode())
        for html_json in json_body["data"]:
            if 'object' in html_json:
                obj = html_json['object']
                if 'excerpt' in obj:
                    best_answer_id = obj['id']
                if 'question' in obj:
                    q_id = obj['question']['id']
                    ques_url = 'https://www.zhihu.com/question/' + q_id
                    yield scrapy.Request(
                        url=ques_url,
                        method='GET',
                        cookies=ZHIHU_COOKIE,
                        callback=self.question_parse,
                        meta={'best_id': best_answer_id, 'q_id': q_id}
                    )

    def question_parse(self, response):
        print("111", response.url)
        question_item = Question_Item(
            q_id=response.meta['q_id'],
            q_title=None,
            q_detail=None,
            q_create_time=None,
            q_attention_num=None,  # 关注者
            answer_num=None,
            q_scanner_num=None,  # 被浏览数
            best_answer_id=response.meta['best_id'],
            url=response.url
        )

        sel = Selector(response)
        question_item['q_title'] = sel.xpath('//div[@class="QuestionHeader-content"]/div/h1/text()').extract_first()
        question_item['q_create_time'] = sel.xpath('//*[@id="root"]/div/main/div/meta[6]/@content').extract_first()

        try:
            question_item['q_detail'] = sel.xpath('//*[@id="root"]/div/main/div/div[1]\
                /div[1]/div[1]/div[1]/div[2]/div/div/div/span/text()').extract()[0]
        except IndexError:
            question_item['q_detail'] = None
        try:
            question_item['q_attention_num'] = re.sub(',', '', sel.xpath(
                '//div[@class="NumberBoard-itemInner"]/strong/text()').extract()[0])
        except IndexError:
            question_item['q_attention_num'] = 0
        try:
            question_item['q_scanner_num'] = int(
                re.sub(',', '', sel.xpath('//div[@class="NumberBoard-itemInner"]/strong/text()').extract()[1]))
        except IndexError:
            question_item['q_scanner_num'] = 0

        try:
            q_answer_num = sel.xpath('//*[@class="List-headerText"]/span/text()').extract()
            qan1 = re.sub(',', '', q_answer_num[0])
            question_item['answer_num'] = int(qan1)
        except IndexError:
            question_item['answer_num'] = 0

        yield question_item
        print("222", question_item)

        if q_answer_num:
            yield Request(url=self.answer_url.format(ques_id=question_item['q_id'], offset=0),
                          method='GET',
                          cookies=ZHIHU_COOKIE,
                          dont_filter=False,
                          callback=self.answer_parse,
                          meta={'q_id': question_item['q_id']}
                          )

    def answer_parse(self, response):
        json_body = json.loads(response.body_as_unicode())['data']
        result = json.loads(response.body_as_unicode())
        qes_id = response.meta['q_id']
        answers_item = answer_Item(
            q_id=qes_id,
            answer_id=None,
            answer_detail=None,
            answer_img=None,
            create_time=None,
            thumb_num=None,
            comment_num=None,
            author_name=None,
            href_num=None
        )
        au_item = author_seeds_Item(
            url_token=None,
            is_crawled=None)

        for i in range(len(json_body)):
            json_arry = json_body[i]
            if json_arry['type'] == 'answer' and ('voteup_count' and 'comment_count') in json_arry:
                answers_item['answer_id'] = json_arry['id']
                create_time = self.change_time(json_arry['created_time'])
                answers_item['create_time'] = create_time
                answers_item['thumb_num'] = json_arry['voteup_count']
                answers_item['comment_num'] = json_arry['comment_count']
                an_content = json_arry['content']
                bs = BeautifulSoup(an_content, "html.parser")
                answers_item['answer_detail'] = bs.get_text()
                img_src = bs.findAll("img", {'class': 'origin_image zh-lightbox-thumb'})
                answers_item['answer_img'] = len(img_src)
                href_num = len(bs.findAll('a'))
                answers_item['href_num'] = href_num
                yield answers_item
                print("333", answers_item)


                if answers_item['comment_num'] != 0:
                    yield Request(url=self.comm_url.format(answer_id=answers_item['answer_id'], offset=0),
                                  method='GET',
                                  callback=self.an_comment_parse,
                                  cookies=ZHIHU_COOKIE,
                                  dont_filter=False,
                                  meta={'answer_id': answers_item['answer_id']}
                                  )

                if 'paging' in result.keys() and result.get('paging').get('is_end') == False:
                    next = result.get('paging').get('next')
                    print("444", next)
                    print("*" * 100)
                    yield Request(
                        url=next,
                        method='GET',
                        dont_filter=False,
                        cookies=ZHIHU_COOKIE,
                        callback=self.answer_parse,
                        meta={'q_id': answers_item['q_id']})

    def an_comment_parse(self, response):
        comment_item = answer_comment_Item(
            answer_id=None,
            comment_detail=None,
            vote_count=None
        )
        comment_item['answer_id'] = response.meta['answer_id']
        json_body = json.loads(response.body_as_unicode())
        data = json_body['data']

        for x in range(0, len(data)):
            content_dic = data[x]
            if content_dic['type'] == 'comment':
                content = content_dic['content']
                bs = BeautifulSoup(content, "html.parser")

                comment_item['comment_detail'] = bs.get_text()
                comment_item['vote_count'] = content_dic['vote_count']
            yield comment_item

            if 'paging' in json_body.keys() and json_body.get('paging').get('is_end') == False:
                next = json_body.get('paging').get('next')
                yield Request(
                    url=next,
                    method='GET',
                    cookies=ZHIHU_COOKIE,
                    dont_filter=False,
                    callback=self.an_comment_parse,
                    meta={'answer_id': comment_item['answer_id']}
                )
