# -*- coding: utf-8 -*-
import scrapy
from scrapy import Field

class Question_Item(scrapy.Item):
    q_id = Field()
    q_title = Field()
    tags = Field()
    q_detail = Field()
    q_create_time = Field()
    q_attention_num = Field()
    answer_num = Field()
    q_scanner_num = Field()
    best_answer_id = Field()
    q_url = Field()
    q_full_name = Field()
    q_alias_name = Field()


class first_answer_Item(scrapy.Item):
    q_id = Field()
    answer_id = Field()
    answer_detail = Field()
    create_time = Field()
    agree_num = Field()
    comment_num = Field()
    href_num = Field()
    reply_which_answer_id = Field()



class second_answer_Item(scrapy.Item):
    answer_id = Field()
    comment_detail = Field()
    vote_count = Field()
