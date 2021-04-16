import scrapy
from scrapy import Request
from scrapy_selenium import SeleniumRequest
from scrapy.loader import ItemLoader
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import time
import json

PATH = "C:\Program Files (x86)\chromedriver.exe"

class MainichiSpider(scrapy.Spider):
    name = "mainichi_selenium_articles"
    start_urls = ["https://mainichi.jp/"]

    def parse(self, response):
        CATEGORIES = {
            "shakai"
            "seiji", 
            "biz",
            "world",
            "sports",
            "science",
            "culture",
            "life",
            "opinion"
        }

        for cat in CATEGORIES: #avoid first category
            link = response.urljoin(cat)
            yield SeleniumRequest(
                url=link, 
                callback=self.collect_articles,
                cb_kwargs=dict(category=cat))

    def collect_articles(self, response, category):
        driver = response.request.meta['driver']
      
        element = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.CSS_SELECTOR, '.link-more')))
        print(f"NEXT BUTTON {element}")
        element.click()
        articles_links = response.css('#article-list a')
        print(f"LINKS FOUND: {len(articles_links.getaall())}")
           
        #articles_links = response.css('#article-list a')
        for link in articles_links:
            l = response.urljoin(link.attrib['href'])
            yield Request(url=l, callback=self.parse_article, cb_kwargs=dict(category=category))

    def parse_article(self, response, category):
        title = response.css('.title-page::text').get()
        paragraphs = response.css('#articledetail-body p::text').getall()
        text = '\n'.join(paragraphs)
        yield {
            "url": response.url,
            "title": title,
            "category": category,
            "text": text
        }



