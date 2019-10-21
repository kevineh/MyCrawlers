import scrapy
from scrapy import Selector
from scrapy import Request
import MySQLdb
from sample.items import SampleItem


class NgaSpider(scrapy.Spider):
    # 这里的name作用是为了运行该爬虫项目，运行时使用命令scrapy crawl NgaSpider而不是scrapy crawl miao(爬虫项目的名称)
    name = "NgaSpider"
    host = "http://yorkbbs.ca/"
    # start_urls是我们准备爬的初始页
    start_urls = "http://forum.yorkbbs.ca/property/"

    custom_settings = {
        'CLOSESPIDER_PAGECOUNT': 1000
    }
    # 定义数据库操作
    # 放在Spider里面可以避免反复连接数据库
    # host = 192.168.0.10
    # port = 32861
    # user = 'root'
    # password = 'wk10142208'
    # db = 'mydata'

    def __init__(self):
        self.connection = MySQLdb.connect(host='192.168.0.10', user='root', password='wk10142208', port=32861,
                                          db='mydata', charset="utf8")
        self.cursor = self.connection.cursor()

    def insert(self, query, params):
        try:
            self.cursor.execute(query, params)
            self.connection.commit()
        except Exception as ex:
            self.connection.rollback()

    def __del__(self):
        self.connection.close()


    # 爬虫的入口，可以在此进行一些初始化工作，比如从某个文件或者数据库读入起始url
    def start_requests(self):
        # 此处将起始url加入scrapy的待爬取队列，并指定解析函数
        # scrapy会自行调度，并访问该url然后把内容拿回来
        yield Request(url=self.start_urls, callback=self.parse_page)

    # 版面解析函数，解析一个版面上的帖子的标题和地址
    def parse_page(self, response):
        selector = Selector(response)
        content_list = selector.xpath('//*[contains(@id,"t_thumbnail")]/a')
        for content in content_list:
            url = self.start_urls + content.xpath('@href').extract_first()
            # 此处，将解析出的帖子地址加入待爬取队列，并指定解析函数
            yield Request(url=url, callback=self.parse_topic)
        # 可以在此处解析翻页信息，从而实现爬取版区的多个页面
        next_page = response.xpath('//*[@id="alltopicpagetop"]/a[text()="下一页\xa0 "]/@href').extract_first()
        if next_page:
            yield scrapy.Request(
                response.urljoin(next_page),
                callback=self.parse_page
            )

    # 帖子的解析函数，解析一个帖子的每一楼的内容
    def parse_topic(self, response):
        selector = Selector(response)
        content_list = selector.xpath('//*[contains(@id,"message")]')
        id_list = selector.xpath('//*[contains(@id,"favatar")]/h3')
        time_list = selector.xpath('//*[@class="toutime"]').xpath('string(.)').re('\d{4}\/[1]*\d\/[1-3]*\d\s[1-2]*\d:[1-5]*\d:[1-5]*\d')
        topic = selector.xpath('//*[@class="V_title f16 fl"]').xpath('string(.)').extract_first()
        for content, uid, time in zip(content_list, id_list, time_list):
            content = content.xpath('string(.)').extract_first()
            uid = uid.xpath('string(.)').extract_first()
            item = SampleItem()
            item['content'] = content
            item['uid'] = uid
            item['reply_date'] = time
            item['topic'] = topic
            yield item

        # 可以在此处解析翻页信息，从而实现爬取帖子的多个页面
        next_page = response.xpath('//*[@class="Pagenum fl"]/a[text()="下一页\xa0 "]/@href').extract_first()
        if next_page:
            yield scrapy.Request(
                response.urljoin(next_page),
                callback=self.parse_page
            )
