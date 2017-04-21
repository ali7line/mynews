# -*- coding: utf-8 -*-
import datetime
import socket

from scrapy.loader import ItemLoader
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from mynews.items import MyyItem


class SomethingSpider(CrawlSpider):
    name = 'red_news'
    allowed_domains = ['reddit.com']
    start_urls = ['https://www.reddit.com/r/programming/']
    

    rules = (
        Rule(LinkExtractor(allow=[r'/r/programming/\?count=(\d+)&after=(\w+)']), callback='parse_item', follow=True),
        )

    def parse_start_url(self, response):
        return self.parse_item(response)


    def parse_item(self, response):
        """scraps info from reddit.com
        @url https://www.reddit.com/r/programming/
        @returns items 25
        @scrapes news_id
        """
        id_list = response.xpath('//div[contains(@class, "thing")]/@id').extract()
        for id_ in id_list:
            l = ItemLoader(item=MyyItem(), response=response)
            l.add_xpath('news_id', id_)
            xpath_header = '//div[@id="{}"]'.format(id_)
            l.add_xpath('title', xpath_header + '//p[@class="title"]/a/text()')
            l.add_xpath('site', xpath_header + '//span[@class="domain"]/a/text()')
            l.add_xpath('link', xpath_header + '//p[@class="title"]/a/@href')
            l.add_xpath('points', xpath_header + '//div[contains(@class, "score") and contains(@class, "unvoted")]/text()', re='[0-9]+')
            l.add_xpath('rank', xpath_header + '//span[@class="rank"]/text()', re='[0-9]+')
            l.add_xpath('author', xpath_header + '//a[contains(@class, "author")]/text()')
            l.add_xpath('comments', xpath_header + '//a[contains(@class, "comments")]', re='[0-9]+')
            l.add_xpath('age', xpath_header + '//time/@datetime')

            l.add_value('url',response.url)
            l.add_value('server',socket.gethostname())
            l.add_value('project',self.settings.get('BOT_NAME'))
            l.add_value('spider',self.name)
            l.add_value('date', datetime.datetime.now())
            yield l.load_item()
