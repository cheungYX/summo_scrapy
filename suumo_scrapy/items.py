# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html
import datetime
import re

import scrapy
from scrapy.loader import ItemLoader
from scrapy.loader.processors import MapCompose, TakeFirst, Join

from w3lib.html import remove_tags
from models.es_types import Article

from elasticsearch_dsl.connections import connections
es = connections.create_connection(hosts=["localhost"])


class ArticleItemLoader(ItemLoader):
    #自定义itemloader
    default_output_processor = TakeFirst()

def remove_t(value):
    return re.sub('\s+', '', value)

def remove_r(value):
    return re.sub('\t', '', value)

def remove_space(value):
    return re.sub(' ', '', value)

def to_space(value):
    return re.sub('\s+', ' ', value)

def to_int(value):
    return int(float(value[0:-2]) * 10000)

def transfer_year(value):
    if value == '新築':
        return 2018
    else:
        return 2018 - int(value[1:-1])

def transfer_area(value):
    return float(value[0:-2])

def stations_formater(value):
    res = []
    stations = value.split()
    for station in stations:
        data = station.split('/')
        dis = re.search('(\d+)分', data[1].split('駅')[1])
        res.append({
            'line' : data[0],
            'station' : data[1].split('駅')[0],
            'distance' : int(dis.group()[0:-1])
        })
        
    return res

class SuumoArticleItem(scrapy.Item):
    # define the fields for your item here like:
    name = scrapy.Field(
        input_processor=MapCompose(remove_tags, remove_t)
    )
    price = scrapy.Field(
        input_processor=MapCompose(remove_tags, remove_t)
    )
    url = scrapy.Field()
    url_object_id = scrapy.Field()

    address = scrapy.Field(
        input_processor=MapCompose(remove_tags, remove_t)
    )
    stations = scrapy.Field(
        input_processor=MapCompose(remove_tags, remove_r, remove_space, to_space)
    )
    size = scrapy.Field(
        input_processor=MapCompose(remove_tags, remove_t)
    )
    area = scrapy.Field(
        input_processor=MapCompose(remove_tags, remove_t)
    )

    build_year = scrapy.Field(
        input_processor=MapCompose(remove_tags, remove_t)
    )
    floor = scrapy.Field(
        input_processor=MapCompose(remove_tags)
    )

    crawl_time = scrapy.Field()

    def save_to_es(self):
        article = Article()
        if self.get('name') is None:
            return
        article.name = self['name']
        article.price = to_int(self.get('price'))
        article.url = self['url']
        article.url_object_id = self['url_object_id']

        article.address = self.get('address')
        article.stations = stations_formater(self.get('stations'))
        article.size = self.get('size')
        article.area = transfer_area(self.get('area'))

        article.build_year = transfer_year(self.get('build_year'))
        if self.get('floor'):
            article.floor = self['floor']
        article.crawl_time = self['crawl_time']

        article.save()

        return
