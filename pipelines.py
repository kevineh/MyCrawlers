# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import MySQLdb

class SamplePipeline(object):
    def open_spider(self, spider):
        self.connection = MySQLdb.connect(host='192.168.0.10', user='root', password='wk10142208', port=32861,
                                          db='mydata', charset="utf8")
        self.cursor = self.connection.cursor()

    def insert(self, query, params):
        try:
            self.cursor.execute(query, params)
            self.connection.commit()
        except Exception as ex:
            self.connection.rollback()

    def close_spider(self, spider):
        self.connection.close()

    def process_item(self, item, spider):
        query = """INSERT INTO YorkBBS (topic, uid, reply_date, content) 
        VALUES (%s, %s, %s, %s)"""
        params = (
            item['topic'], item['uid'], item['reply_date'], item['content']
        )
        spider.insert(query, params)
        return item
