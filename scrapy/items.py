# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class LegisItem(scrapy.Item):
    
    Chapter = scrapy.Field()
    Url = scrapy.Field()
    Content = scrapy.Field()
