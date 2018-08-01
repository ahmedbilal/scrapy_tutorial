import scrapy
from scrapy.utils.response import open_in_browser

class JSTrackScrap(scrapy.Spider):
    name = 'jstrackscrap'
    start_urls = ['https://www.jquery.com',]

    def print_js(self, response):
        page = response.url.split("/")[-1]
        filename = '%s' % page
        with open(filename, 'wb') as f:
            f.write(response.body)

    def parse(self, response):
        for js in response.xpath("//script[contains(@src, '.js')]"):
            link = js.xpath('@src').extract_first()
            if link[:2] == '//':
                link = 'http:' + link
            yield scrapy.Request(link, callback=self.print_js)
