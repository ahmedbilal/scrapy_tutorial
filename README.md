## How to run quotes crawler? (basic scrappy task)
**Fetches quotes from quotes.toscrape.com**

```bash
cd tutorial
rm quotes.jl; scrapy crawl quotes -o quotes.jl
```


## How to run author crawler? (basic scrappy task)
**Fetches quotes' author bio from quotes.toscrape.com**


```bash
cd tutorial
rm authors.jl; scrapy crawl author -o authors.jl
```


## How to run github emails crawler (scrappy session task)?

**You need to enter your username and password in spiders/github_emails.py. It will output your emails you listed in your github**


```bash
cd tutorial
rm emails.jl; scrapy crawl emails -o emails.jl
```


## How to run js_track_scrap crawler (scrappy js tracking and replicating task)?
**It finds all js files referred by script tag in a given url and download them**
```bash
cd tutorial
scrapy crawl jstrackscrap
```

## How to run github_repos crawler (post request, session management and recovery task)
**Github-repos spider log in to Github and fetches all of user's repo links.
Then it have to go to each repo's setting and fetches its name. But, the twist is that we will break session(remove cookies) with some random probability before accessing repo's setting (thus creating an effect that the website break our session due to some reason).
The crawler should know that session is broken and should restablish it**

**Note:** Insert your github username and password at line#46 of **spiders/github-repos.py**
```bash
clear; rm repo_description.jl; scrapy crawl github-repos -o repo_description.jl
```