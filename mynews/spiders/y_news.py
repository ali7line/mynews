# -*- coding: utf-8 -*-
import datetime
import socket

from scrapy.loader import ItemLoader
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from mynews.items import MyyItem


class SomethingSpider(CrawlSpider):
    name = 'y_news'
    allowed_domains = ['news.ycombinator.com']
    start_urls = ['http://news.ycombinator.com/']
    

    rules = (
        Rule(LinkExtractor(restrict_xpaths='//a[@class="morelink"]'), callback='parse_item', follow=True),
        )

    def parse_start_url(self, response):
        return self.parse_item(response)


    def parse_item(self, response):
        """scraps info from news.ycombinator.com
        @url http://news.ycombinator.com
        @returns items 30
        @scrapes news_id
        """
        page_id = response.xpath('//tr[@class="athing"]/@id').extract()
        for news_id in page_id:
            l = ItemLoader(item=MyyItem(), response=response)
            l.add_xpath('news_id', news_id)
            xpath_header = '//*[@id="{}"]'.format(news_id)
            l.add_xpath('title', xpath_header + '/td[3]/a/text()')
            l.add_xpath('site', xpath_header + '//span[@class="sitestr"]/text()')
            l.add_xpath('link', xpath_header + '//a[@class="storylink"]/@href')
            l.add_xpath('author', xpath_header + '/following-sibling::tr[1]/td[@class="subtext"]/a[1]/text()')
            l.add_xpath('points', '//*[@id="score_{}"]/text()'.format(news_id), re='[0-9]+')
            l.add_xpath('rank', xpath_header + '/td[1]/span/text()', re='[0-9]+')
            l.add_xpath('comments', xpath_header + '/following-sibling::tr[1]/td[@class="subtext"]/a[3]/text()', re='[0-9]+')
            l.add_xpath('age', xpath_header + '/following-sibling::tr[1]//span[@class="age"]/a/text()')

            l.add_value('url',response.url)
            l.add_value('server',socket.gethostname())
            l.add_value('project',self.settings.get('BOT_NAME'))
            l.add_value('spider',self.name)
            l.add_value('date', datetime.datetime.now())
            yield l.load_item()
