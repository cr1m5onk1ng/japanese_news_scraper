# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from itemloaders.processors import MapCompose


def remove_sitemap_ref(link: str):
    return '/'.join(link.split("/")[:-1] + ["list"])

class AsahiTopicItem(scrapy.Item):
    link = scrapy.Field(input_processor=MapCompose(remove_sitemap_ref))
    topic = scrapy.Field()
    
