import scrapy
from scrapy.loader import ItemLoader
from scrapy.loader.processors import TakeFirst, Join

class Author(scrapy.Item):
    name = scrapy.Field()
    born = scrapy.Field()
    description = scrapy.Field()


class AuthorLoader(ItemLoader):
    def two_sentences_only(self, values):
        for v in values:
            sec_sen_end_index = v.find(".")  # end of first sentence
            sec_sen_end_index = v.find(".", sec_sen_end_index + 1) # end of first sentence
            yield v[:sec_sen_end_index].strip()  # strip newlines
    
    default_output_processor = TakeFirst()
    born_out = Join()  # because there are two born properties (born_date, born_location)
    description_in = two_sentences_only  # we want only two sentences of description

class AuthorSpider(scrapy.Spider):
    name = 'author'
    start_urls = ['http://quotes.toscrape.com/page/1/']

    def parse(self, response):
        for quote in response.xpath("//div[@class='quote']"):
            author_page_link = quote.xpath("span[small[@class='author']]/a/@href").extract_first()
            yield response.follow(author_page_link,  callback=self.parse_author)
        
        next_page = response.xpath("//li[@class='next']/a/@href").extract_first()
        yield response.follow(next_page, callback=self.parse)


    def parse_author(self, response):
        l = AuthorLoader(item=Author(), response=response)
        l.add_xpath('name', xpath="//h3[@class='author-title']/text()")
        l.add_xpath('born', xpath="//span[@class='author-born-date']/text()")
        l.add_xpath('born', xpath="//span[@class='author-born-location']/text()")
        l.add_xpath('description', xpath="//div[@class='author-description']/text()")

        yield l.load_item()
