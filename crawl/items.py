# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class YoutubeListItem(scrapy.Item):
    name = scrapy.Field()
    link = scrapy.Field()


class KBSRadioItem(scrapy.Item):
    subject = scrapy.Field()
    content = scrapy.Field()
    num = scrapy.Field()
    writer = scrapy.Field()
    date = scrapy.Field()
    inquery = scrapy.Field()
    recommend = scrapy.Field()
