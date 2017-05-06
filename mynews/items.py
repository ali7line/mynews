# -*- coding: utf-8 -*-
from scrapy.item import Item, Field


class MyyItem(Item):
    # main info from ycombinator
    news_id = Field()
    title = Field()
    site = Field()
    link = Field()
    author = Field()
    points = Field()
    rank = Field()
    tags = Field()
    comments = Field()
    age = Field()

    # housekeeping
    url = Field()
    server = Field()
    project = Field()
    spider = Field()
    date = Field()
