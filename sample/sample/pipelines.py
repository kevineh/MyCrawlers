# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


class SamplePipeline(object):
    def process_item(self, item, spider):
        query = """INSERT INTO YorkBBS (topic, uid, reply_date, content) 
        VALUES (%s, %s, %s, %s)"""
        params = (
            item['topic'], item['uid'], item['reply_date'], item['content']
        )
        spider.insert(query, params)
        return item
