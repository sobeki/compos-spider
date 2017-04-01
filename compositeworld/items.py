# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class CompositeworldItem(scrapy.Item):
    website_link = scrapy.Field()
    company_name = scrapy.Field()
    city = scrapy.Field()
    state = scrapy.Field()
    product = scrapy.Field()
    description = scrapy.Field()
    
