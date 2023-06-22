import scrapy

API_KEY = '5591c5dc-56fe-4a6a-bb72-b929f51ee277'
from urllib.parse import urlencode

from bookscraper.items import BookItem

import random

# function that help us send the traffic first to our proxy provider
# Whith the URL (of the site that we want to scrape) and with the API_KEY we're going to create a new proxy_url
def get_proxy_url(url):
    payload = {'api_key': API_KEY, 'url': url}
    proxy_url = 'https://proxy.scrapeops.io/v1/?' + urlencode(payload)
    return proxy_url


class BookspiderSpider(scrapy.Spider):
    name = "bookspider"
    allowed_domains = ["books.toscrape.com", "proxy.scrapeops.io"]
    start_urls = ["https://books.toscrape.com"]

    custom_settings = {
        'FEEDS': {
            'bookdata.json': {'format': 'json', 'overwrite': True},
        }
    }

    # When the spider starts up run this function and this function run our guess proxy URL
    def start_requests(self):
        yield scrapy.Request(url=get_proxy_url(self.start_urls[0]), callback=self.parse)

    def parse(self, response):
        books = response.css('article.product_pod')

        for book in books:
            relative_url = books.css('h3 a::attr(href)').get()

            if 'catalogue/' in relative_url:
                book_url = 'http://books.toscrape.com/' + relative_url
            else:
                book_url = 'http://books.toscrape.com/catalogue/' + relative_url

            # yield response.follow(book_url, callback=self.parse_book_page)
            yield scrapy.Request(url=get_proxy_url(book_url), callback=self.parse_book_page)

        #     yield {
        #         'name': book.css('h3 a::text').get(),
        #         'price': book.css('.product_price .price_color::text').get(),
        #         'url': book.css('h3 a').attrib['href']
        #     }
        #
        next_page = response.css('li.next a::attr(href)').get()
        if next_page is not None:
            if 'catalogue/' in next_page:
                next_page_url = 'http://books.toscrape.com/' + next_page
            else:
                next_page_url = 'http://books.toscrape.com/catalogue/' + next_page

            # yield response.follow(next_page_url, callback=self.parse)
            yield scrapy.Request(url=get_proxy_url(next_page_url), callback=self.parse)


    def parse_book_page(self, response):
        table_rows = response.css("table tr")
        book_item = BookItem()


        book_item['url'] = response.url,
        book_item['title'] = response.css('.product_main h1::text').get(),
        book_item['upc'] = table_rows[0].css("td ::text").get(),
        book_item['product_type'] = table_rows[1].css("td ::text").get(),
        book_item['price_excl_tax'] = table_rows[2].css("td ::text").get(),
        book_item['price_incl_tax'] = table_rows[3].css("td ::text").get(),
        book_item['tax'] = table_rows[4].css("td ::text").get(),
        book_item['availability'] = table_rows[5].css("td ::text").get(),
        book_item['num_reviews'] = table_rows[6].css("td ::text").get(),
        book_item['stars'] = response.css("p.star-rating").attrib['class'],
        book_item['category'] = response.xpath("/html/body/div/div/ul/li[3]/a/text()").get(),
        book_item['description'] = response.xpath("/html/body/div/div/div[2]/div[2]/article/p/text()").get(),
        book_item['price'] = response.css('p.price_color ::text').get(),

        yield book_item