course tutorial bookscraper
This project is for know how works scrappy in order to scrap a web site 

First Steps

1. create a virtual enviroment

`python3 -m venv vevnscrapy`

1.1 activate virtual environment

`source vevnscrapy/bin/activate`

2. install scrapy

`pip install scrapy`

3. start scrapy project

`scrapy startproject bookscraper`

3.1 after execute this command the directory *bookscraper* will be created

---

**CREATE A SPIDER**

inside *spiders* directory `~/bookscraper/bookscraper/spider` run the next command

`scrapy genspider bookspider books.toscrape.com`

where:
bookspider ==> name of spider
books.toscrape.com ==> web site URL for scraping


**USE SCRAPY SHELL**

install ipython

`python install ipython`

run scrapy shell

`scrapy shell`

*TERMINAL SCRAPY*

1: `fetch('https://books.toscrape.com')`

2: `response`

3: `response.css('article.product_pod')` # return all the article labels (books) in the page

4: `response.css('article.product_pod').get()` #get the first article HTML content

5: `books = response.css('article.product_pod')` # put all books in a diferente variable 

6: `len(books)` # total books in page obtained
