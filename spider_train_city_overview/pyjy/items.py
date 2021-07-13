# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class PyjyItem(scrapy.Item):
    # define the fields for your item here like:
    train_id = scrapy.Field()
    departure_city = scrapy.Field()
    arrival_city = scrapy.Field()
    departure_station= scrapy.Field()
    arrival_station= scrapy.Field()
    train_start_date= scrapy.Field()
    departure_time= scrapy.Field()
    arrival_time= scrapy.Field()
    duration_time= scrapy.Field()
    pass_city= scrapy.Field()
    train_num=scrapy.Field()



