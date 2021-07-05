# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class PyjyItem(scrapy.Item):
    # define the fields for your item here like:
    title = scrapy.Field()
    # id
    #id= scrapy.Field()
    #航空公司
    content = scrapy.Field()



