# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

from scrapy import Item, Field


class SampleItem(Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    topic = Field()
    reply_date = Field()
    uid = Field()
    content = Field()



