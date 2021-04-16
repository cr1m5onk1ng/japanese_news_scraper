import scrapy
from news_scraper.items import AsahiTopicItem
from scrapy import Request
from scrapy.loader import ItemLoader

class AsahiTopicSpider(scrapy.Spider):
    name = "asahi_topics"
    start_urls = ["https://www.asahi.com/sitemap"]

    def parse(self, response):
        topics = response.css('div.SitemapListBlock')
        categories = topics.css('h3')
        #links = categories.css('a')
        
        for cat in categories:
            il = ItemLoader(item=AsahiTopicItem(), selector=cat)
            il.add_css('link', 'a::attr(href)')
            il.add_css('topic', 'a::attr(custom)')
            #item["link"] = l.attrib['href']
            #item["topic"] = l.attrib['custom']
            #yield item
            yield il.load_item()


class AsahiArticlesSpider(scrapy.Spider):
    name = "asahi_articles"
    
    def start_requests(self):
        urls = [
            "http://www.asahi.com/national/list",
            "http://www.asahi.com/politics/list",
            "http://www.asahi.com/business/list",
            "http://www.asahi.com/international/list",
            "http://www.asahi.com/sports/list",
            "http://www.asahi.com/tech_science/list"
            "http://www.asahi.com/culture/list", 
            "http://www.asahi.com/edu/list",
            "http://www.asahi.com/eco/list", 
            "http://www.asahi.com/opinion/list"
            "http://www.asahi.com/apital/list"
        ]
        for url in urls:
            cat = url.split("/")[-2]
            yield scrapy.Request(url=url, callback=self.parse, cb_kwargs=dict(category=cat))

    def parse(self, response, category):
        links = response.css('.SectionFst a')
        for l in links:
            link = response.urljoin(l.attrib['href'])
            yield Request(link, callback=self.parse_article, cb_kwargs=dict(category=category))

    def parse_article(self, response, category):
        title = response.css('#MainInner h1::text').get()
        paragraphs = response.css('.ArticleText p::text').getall()
        text = "\n".join(paragraphs)
        yield {
            "title": title,
            "text": paragraphs,
            "category": category
        }


