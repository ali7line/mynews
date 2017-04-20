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
        selector_list = response.css('div.thing')
                
        for selector in selector_list:
            item = MyyItem()
            #item['image_urls'] = selector.xpath('a[contains(@class, "thumbnail")]/@href').extract()
            item['title'] = selector.xpath('div/p/a/text()').extract()
            item['link'] = selector.xpath('a/@href').extract()
                    
            yield item

        #page_id = response.xpath('//tr[@class="athing"]/@id').extract()
        #for news_id in page_id:
        #    l = ItemLoader(item=MyyItem(), response=response)
        #    l.add_xpath('news_id', news_id)
        #    xpath_header = '//*[@id="{}"]'.format(news_id)
        #    l.add_xpath('title', xpath_header + '/td[3]/a/text()')
        #    l.add_xpath('site', xpath_header + '//span[@class="sitestr"]/text()')
        #    l.add_xpath('link', xpath_header + '//a[@class="storylink"]/@href')
        #    l.add_xpath('author', xpath_header + '/following-sibling::tr[1]/td[@class="subtext"]/a[1]/text()')
        #    l.add_xpath('points', '//*[@id="score_{}"]/text()'.format(news_id), re='[0-9]+')
        #    l.add_xpath('rank', xpath_header + '/td[1]/span/text()', re='[0-9]+')
        #    l.add_xpath('comments', xpath_header + '/following-sibling::tr[1]/td[@class="subtext"]/a[3]/text()', re='[0-9]+')
        #    l.add_xpath('age', xpath_header + '/following-sibling::tr[1]//span[@class="age"]/a/text()')

        #    l.add_value('url',response.url)
        #    l.add_value('server',socket.gethostname())
        #    l.add_value('project',self.settings.get('BOT_NAME'))
        #    l.add_value('spider',self.name)
        #    l.add_value('date', datetime.datetime.now())
        #    yield l.load_item()
