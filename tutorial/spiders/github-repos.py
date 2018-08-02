import scrapy
from scrapy.utils.response import open_in_browser
from scrapy.http import Request
import random

class GithubRepos(scrapy.Spider):
    name = 'github-repos'
    start_urls = ['https://github.com/settings/repositories']
    logout_url = 'https://github.com/logout'
    login_url = 'https://github.com/login'
    def parse(self, response):
        if b"Signed in as" in response.body:
            self.logger.info("User Logged in")
            for repo in response.css(".js-collab-repo"):
                repo_name = repo.css("a::text").extract_first()
                repo_name = repo_name.split("/")[1]  # username/"repository"
                print("REPO:", repo_name)
                repo_link = repo.css("a::attr(href)").extract_first()
                
                if random.random() < 0.3:
                    yield response.follow(repo_link + '/settings', 
                    meta={'url':response.urljoin(repo_link) + '/settings',
                    'dont_redirect': True,
                    'handle_httpstatus_all':True,
                    'dont_merge_cookies': True},
                    callback=self.read_name_from_settings,
                    dont_filter = True)
                else:
                    yield response.follow(repo_link + '/settings', 
                    meta={'url':response.urljoin(repo_link) + '/settings',
                    'dont_redirect': True,
                    'handle_httpstatus_all':True},
                    callback=self.read_name_from_settings,
                    dont_filter = True)
        else:
            self.logger.info("User not logged in")
            yield Request(self.login_url, callback=self.login, meta={'url':self.start_urls[0]},
            dont_filter = True)


    def login(self, response):
        authenticity_token = response.css("form input[name='authenticity_token']::attr(value)").extract_first()
        print("authenticity: ", authenticity_token)
        print("Logging for", response.meta['url'])
        return scrapy.FormRequest.from_response(response,
        formdata={'login':'meowmeow', 'password':'meow'},
        callback=self.is_login_successfull,
        meta = {'url': response.meta['url']},
        dont_filter = True)

    def is_login_successfull(self, response):
        if b'Incorrect username' in response.body:
            self.logger.error("Invalid username or password")
            yield {'Message': 'Please write your github username and password at github_emails/spiders/github_emails.py at line 12'}
        else:  # success
            self.logger.info("Logged in successfully")
            if response.meta['url'] == self.start_urls[0]:
                yield scrapy.Request(self.start_urls[0],callback=self.parse, dont_filter = True)
            else:
                yield Request(response.meta['url'], callback=self.read_name_from_settings, dont_filter = True)

    def read_name_from_settings(self, response):
        print("HTTP Status", response.status)
        if b"Signed in as" in response.body:
            repo_name = response.url.split("/")[4]  # http://website.domain/username/repository/settings
            repo_name_from_settings = response.css("input[id='rename_field']::attr(value)").extract_first()

            yield { repo_name: repo_name_from_settings }
        
        else:
            self.logger.info("User not logged in - read_name_from_settings")
            print("calling login with url", response.meta['url'])
            yield Request(self.login_url, callback=self.login, meta={'url':response.meta['url']}, dont_filter = True)
