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

                # authenticity_token = response.css("form[class='logout-form'] input[name='authenticity_token']::attr(value)").extract_first()
                # logout_form_data = {"authenticity_token": authenticity_token}
                # yield scrapy.FormRequest.from_response(response, callback=self.dead, meta={'dont_redirect': True, 'handle_httpstatus_all':True}, formcss="form[class='logout-form']", method='POST', formdata=logout_form_data)
            
                yield response.follow(repo_link + '/settings', meta={'dont_redirect': True, 'handle_httpstatus_all':True}, callback=self.read_name_from_settings)
        else:
            self.logger.info("User not logged in")
            yield Request(self.login_url, callback=self.login)


    def login(self, response):
        authenticity_token = response.css("form input[name='authenticity_token']::attr(value)").extract_first()
        print("authenticity: ", authenticity_token)
        return scrapy.FormRequest.from_response(response,
        formdata={'login':'ahmedbilal', 'password':'ahmedbilalkhalid'},
        callback=self.is_login_successfull
        )

    def is_login_successfull(self, response):
        if b'Incorrect username' in response.body:
            self.logger.error("Invalid username or password")
            yield {'Message': 'Please write your github username and password at github_emails/spiders/github_emails.py at line 12'}
        else:  # success
            self.logger.info("Logged in successfully")
            yield scrapy.Request('https://github.com/settings/repositories',callback=self.parse)

    def read_name_from_settings(self, response):
        # authenticity_token = response.css("form[class='logout-form'] input[name='authenticity_token']::attr(value)").extract_first()
        # logout_form_data = {"authenticity_token": authenticity_token}
        # yield scrapy.FormRequest.from_response(response, callback=self.dead, meta={'dont_redirect': True, 'handle_httpstatus_all':True}, formcss="form[class='logout-form']", method='POST', formdata=logout_form_data)
        # logged_out = True    
        print("HTTP Status", response.status)
        if b"Signed in as" in response.body:
            repo_name = response.url.split("/")[4]  # http://website.domain/username/repository/settings
            repo_name_from_settings = response.css("input[id='rename_field']::attr(value)").extract_first()

            yield { repo_name: repo_name_from_settings }
        
        else:
            self.logger.info("User not logged in")
            yield scrapy.Request(self.login_url, callback=self.login)

        authenticity_token = response.css("form[class='logout-form'] input[name='authenticity_token']::attr(value)").extract_first()
        logout_form_data = {"authenticity_token": authenticity_token}
        yield scrapy.FormRequest.from_response(response, callback=self.dead, meta={'dont_redirect': True, 'handle_httpstatus_all':True}, formcss="form[class='logout-form']", method='POST', formdata=logout_form_data)
        
    
    def dead(self, response):

        print("Logged out")
        return None