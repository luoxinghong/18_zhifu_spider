# -*- coding: utf-8 -*-
import scrapy
from scrapy import Field

class Question_Item(scrapy.Item):
    q_id = Field()
    q_title = Field()
    q_detail = Field()
    # question_time=Field()
    q_create_time = Field()
    q_attention_num = Field()
    answer_num = Field()
    q_scanner_num = Field()
    best_answer_id = Field()
    url = Field()


class answer_Item(scrapy.Item):
    q_id = Field()
    answer_id = Field()
    answer_detail = Field()
    answer_img = Field()
    create_time = Field()
    thumb_num = Field()
    comment_num = Field()
    author_name = Field()
    href_num = Field()


class answer_comment_Item(scrapy.Item):
    answer_id = Field()
    comment_detail = Field()
    vote_count = Field()


class author_seeds_Item(scrapy.Item):
    url_token = Field()
    is_crawled = Field()
