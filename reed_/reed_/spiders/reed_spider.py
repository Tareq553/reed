import scrapy
import numpy as np
import requests
from bs4 import BeautifulSoup
from ..items import ReedItem



class ReedSpiderSpider(scrapy.Spider):
    name = 'reed_spider'
    page_number= 2
    start_urls = [
        'https://www.reed.co.uk/courses/all?pageno=1&pagesize=100'
    ]

    def parse(self, response):
        items = ReedItem()
        for all in response.css(".search-card-variant-details-top-col"):
            link=all.css(".search-card-variant-title a::attr(href)").get()

            yield {
                'course_link': link
            }
        r = requests.get("https://www.reed.co.uk/courses/all?pageno=1&sortby=MostPopular&pagesize=100")
        s = BeautifulSoup(r.text, "lxml")
        totalCourse = int(s.find("span", class_="h1").text.strip().replace(",", ""))
        totalPage = int(np.ceil(totalCourse / 100))
        next_page="https://www.reed.co.uk/courses/all?pageno="+str(ReedSpiderSpider.page_number)+"&pagesize=100"
        if ReedSpiderSpider.page_number<totalPage:
            ReedSpiderSpider.page_number +=1
            yield response.follow(next_page,callback = self.parse)

