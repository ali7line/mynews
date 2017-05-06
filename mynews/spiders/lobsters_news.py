# -*- coding: utf-8 -*-
import datetime
import socket

from scrapy.loader import ItemLoader
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from mynews.items import MyyItem

rank = 0

class SomethingSpider(CrawlSpider):
    name = 'lobsters_news'
    allowed_domains = ['lobste.rs']
    start_urls = ['https://lobste.rs/']
    

    rules = (
        Rule(LinkExtractor(allow=[r'/page/(\d+)']), callback='parse_item', follow=True),
        )

    def parse_start_url(self, response):
        return self.parse_item(response)


    def parse_item(self, response):
        """scraps info from reddit.com
        @url https://www.reddit.com/r/programming/
        @returns items 25
        @scrapes news_id
        """
        id_list = response.xpath('//li[contains(@class, "story")]/@data-shortid').extract()
        for id_ in id_list:
            global rank
            rank += 1
            l = ItemLoader(item=MyyItem(), response=response)
            # l.add_value('news_id', "".join('story_', id_)) ## done
            xpath_header = '//li[@id="story_{}"]'.format(id_) ## done
            print(xpath_header, '--------------------------------------------<<<<')
            l.add_xpath('title', xpath_header + '//span[@class="link"]/a/text()') ## done
            l.add_xpath('tags', xpath_header + '//a[contains(@class,"tag")]/text()') ## done
            l.add_xpath('site', xpath_header + '//a[@class="domain"]/text()') ## done
            l.add_xpath('link', xpath_header + '//span[@class="link"]/a/@href') ## done
            l.add_xpath('points', xpath_header + '//div[@class="score"]/text()', re='[0-9]+') ## done
            l.add_value('rank', rank) ## done
            l.add_xpath('author', xpath_header + '//img[@class="avatar"]/following::a[1]/text()') ## done
            l.add_xpath('comments', xpath_header + '//span[@class="comments_label"]/a/text()', re='[0-9]+') ## done
            l.add_xpath('age', xpath_header + '//div[@class="byline"]//span[1]/@title') ## done

            l.add_value('url',response.url)
            l.add_value('server',socket.gethostname())
            l.add_value('project',self.settings.get('BOT_NAME'))
            l.add_value('spider',self.name)
            l.add_value('date', datetime.datetime.now())
            yield l.load_item()
