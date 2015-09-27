# -*- coding: utf-8 -*-
import scrapy
import re
from scrapy.spiders import CrawlSpider, Rule
from crawl.items import YoutubeListItem, KBSRadioItem
from scrapy.linkextractors import LinkExtractor
from scrapy.linkextractors.lxmlhtml import LxmlLinkExtractor

class CommonSpider(scrapy.Spider):
    name = "common"
    allowed_domains = ["common.com"]
    start_urls = (
        'http://www.common.com/',
    )

    def parse(self, response):
        pass


class YoutubeListSpider(scrapy.Spider):
    name = "youtubelist"
    allowed_domains = ["youtube.com"]
    start_urls = (
        'https://www.youtube.com/watch?v=a7HMg8YkR2s&list=PLJMkXde6QnszTaA8mYLsrO7lUNkUkF_RZ',
    )

    def parse(self, response):
        links = []
        for ele in response.css(".playlist-videos-container").xpath(
                "//div/a[contains(@href, '/watch')]/@href"):
            if re.search('watch\?v=[a-zA-Z_]+', ele.extract()):
                links.append(ele.extract())

        links = set(links)
        for link in links:
            item = YoutubeListItem()
            item['name'] = 'name'
            item['link'] = re.findall(
                'watch\?v=([a-zA-Z_0-9-]*)', link)[0]

            yield item


def kbs_process_value(value):
    m = re.search("javascript:ViewArticle\(([0-9]+),([0-9]+)\)", value)
    link_templage = 'http://www.cbs.co.kr/radio/pgm/board.asp?pn=read&skey=&sval=&anum=%s&vnum=%s&bgrp=2&page=&bcd=01000295&pgm=263&mcd=BOARD6'

    if m:
        vnum, anum = m.group(1), m.group(2)
        return link_templage % (anum, vnum)

    
class KBSRadioSpider(CrawlSpider):
    name = "kbsradio"
    allowed_domains = ["www.cbs.co.kr"]
    start_urls = (
        'http://www.cbs.co.kr/radio/pgm/board.asp?pn=list&skey=&sval=&bgrp=2&page=&bcd=01000295&pgm=262&mcd=BOARD6',
    )

    rules = [
        # Rule(
        #     LinkExtractor(allow=['page=\d' ])),
        Rule(
            LxmlLinkExtractor(process_value=kbs_process_value), callback='parse_item'
            )
        ]

    def parse_item(self, response):
        item = KBSRadioItem()
        item['content'] = ''.join(response.xpath('//td[contains(@class, "bd_article")]/text()').extract()).replace('\r\n\r\n','\r\n')
        bd_menu_content = response.xpath('//td[contains(@class, "bd_menu_content")]/text()').extract()

        item['subject'] = bd_menu_content[0]
        item['num'] = bd_menu_content[1]
        item['writer'] = bd_menu_content[2]
        item['date'] = bd_menu_content[3]
        item['inquery'] = bd_menu_content[4]
        item['recommend'] = bd_menu_content[5]
        print item
        yield item

