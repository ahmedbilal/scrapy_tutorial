import scrapy

class QuotesSpider(scrapy.Spider):
    name = "quotes"

    start_urls = ['http://quotes.toscrape.com/page/1/']

    def parse(self, response):
        for quote in response.xpath("//div[@class='quote']"):
            to_be_inserted = {}
            text = quote.xpath("string(span[@class='text'])").extract_first().replace("\u201c", "").replace("\u201d", "")
            author = quote.xpath("string(span[2]/small)").extract_first()
            tags = quote.xpath("div[@class='tags']")

            to_be_inserted['text'] = text
            to_be_inserted['author'] = author
            to_be_inserted['tags'] = tags.xpath("string(a[@class='tag'])").extract()
##            for tag in tags.xpath("a[@class='tag']"):
##                _tag = tag.xpath('string(.)').extract()
##                if to_be_inserted.get('tags', None) == None:
##                    to_be_inserted['tags'] = [_tag]
##                else:
##                    to_be_inserted['tags'].append(_tag)
            yield to_be_inserted

            relative_url = response.xpath("//ul[@class='pager']/li[@class='next']/a/@href").extract_first()
            if relative_url:
                yield response.follow(relative_url, callback=self.parse)
            
