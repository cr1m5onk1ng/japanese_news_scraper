import scrapy
from scrapy import Request
from scrapy.loader import ItemLoader


class NikkeiSpider(scrapy.Spider):
    name = "nikkei_articles"
    start_urls = ["https://www.nikkei.com/"]

    def start_requests(self):
        """
        CATEGORIES = ["economy", "politics", "business", "technology", "international", "opinion",
                        "sports", "society", "local", "culture"]
        """
        CATEGORIES = ["money", "economy", "business", "markets", "opinion",
                        "sports", "local", "culture"]
        input_category = getattr(self, "cat", None)
        if input_category is not None:
            CATEGORIES = [input_category]
        base_url = "https://www.nikkei.com/"
        for cat in CATEGORIES:
            url = base_url + cat + "/archive"
            yield scrapy.Request(url=url, callback=self.parse, cb_kwargs=dict(category=cat))

    def parse(self, response, category):
        links = response.css('.m-miM09_title > a')
        for l in links:
            reference = l.attrib['href']
            yield Request(url=response.urljoin(reference), callback=self.parse_article,  cb_kwargs=dict(category=category))
        pages = response.css('.m-pageNation a')
        if pages is not None:
            yield from response.follow_all(pages, callback=self.parse, cb_kwargs=dict(category=category))

    def parse_article(self, response, category):
        title = response.css('.title_tyodebu::text').get()
        paragraphs = response.css('.paragraph_puhrdq0::text').getall()
        text = "\n".join(paragraphs)
        yield {
            "url": response.url,
            "title": title,
            "text": text,
            "category": category
        }
