# -*- coding: utf-8 -*-
import os
from subprocess import call

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


class YoutubeListPipeline(object):
    def process_item(self, item, spider):
        os.chdir(os.path.expanduser('~/Music'))
        call(["youtube-dl", "--extract-audio",
              "--audio-format",
              "mp3", item['link']])
        return item
