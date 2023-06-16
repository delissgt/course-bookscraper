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

```
# get the name, price and URL for the first book

book = books[0]

# getting title 
book.css('h3 a::text').get() # 'A light in the ...'

#getting price 
book.css('.product_price .price_color::text').get() # '&51.77'

#getting link 
book.css('h3 a').attrib['href']
```

**EXECUTE SPIDER**

* `scrapy crawl bookspider`
 
 bookspider == spider_name
 
 
* `scrapy crawl bookspider -O bookdata.csv`
* `scrapy crawl bookspider -O bookdata.json`

 save data into a file .csv and .json using -O (capital letter) Overwrite
 
 
* `scrapy crawl bookspider -o bookdata.csv`
* `scrapy crawl bookspider -o bookdata.json`

 append data into a file .csv and .json using -o 

`scrapy list`

list spiders


# Pipelines

use for clean the data.
For example remove the currency signs
convert the price from pounds to dollars
format strings to integers (if you are going to save it into a database that becomes very important)
converting relative URLs to full URLs
Validate data, check if price is actually a price or is it sold out, and then you can know put price in price of zero
Store data instead a file get the data to go directly into a database

NOTE:

remember uncomment or add the next line in **setting.py**

```python
# Configure item pipelines
# See https://docs.scrapy.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
   "bookscraper.pipelines.BookscraperPipeline": 300,
}

```

# Saving Data to Files & Databases

In File **setting.py** add the next lines

```python
FEEDS = {
   'bookdata.json': {'format': 'json'}
}
```

This lines output the data cleaned in a file called *bookdata.json*

So instance use `scrapy crawl bookspider -O bookdata.json` 
we just need to run the next command

 ```python
scrapy crawl bookspider
```

and the file *bookdata.json* will automatically generated 


Add next file in *bookspider.py*

```python
class BookspiderSpider(scrapy.Spider):
    ...
    start_urls = ["https://books.toscrape.com"]
    ...

    custom_settings  = {
        'FEEDS' : {
            'bookdata.json': {'format': 'json', 'overwrite': True}
        }
    }
```

This enable overwrite anything you have in *settings* file
and you can specify it in the spider.
We need to specify what we want to overwrite.
If it sees that the feeds are set here it will overwrite what we have in our *settings.py* file.
This is an easy way that if you want to specify certain settings you can do them here. 
They don't all have to be in *settings.py* file


