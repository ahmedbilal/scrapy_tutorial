import scrapy
from scrapy.utils.response import open_in_browser
from scrapy.http import Request
class GithubEmails(scrapy.Spider):
    name = 'emails'
    start_urls = ['https://github.com/login',]

    def parse(self, response):
        self.logger.error("Hello")
        return scrapy.FormRequest.from_response(
            response,
            formdata={'login':'meowmeow', 'password':'meow'},
            callback=self.after_login
        )

    def after_login(self, response):
        if b'Incorrect username' in response.body:
            self.logger.error("Invalid username or password")
            yield {'Message': 'Please write your github username and password at github_emails/spiders/github_emails.py at line 12'}
        else:  # success
            emails_page = scrapy.Request('https://github.com/settings/emails',callback=self.get_login)
            self.logger.info("Logged in successfully")
            yield emails_page

    def get_login(self, response):
        for email in response.xpath("//ul[@id='settings-emails']/li[contains(@class, 'settings-email')]"):
            extracted_email = email.xpath("span[contains(@title, '@')]/text()").extract_first()
            yield {'email': extracted_email }
