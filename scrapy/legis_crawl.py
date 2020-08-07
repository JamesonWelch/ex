# -*- coding: utf-8 -*-
import scrapy
from legis.items import LegisItem
from scrapy.http import Request


class LegisCrawlSpider(scrapy.Spider):
    name = 'legis_crawl'
    start_urls = ['http://alisondb.legislature.state.al.us/alison/codeofalabama/1975/13297.htm']

    BASE_URL = 'http://alisondb.legislature.state.al.us/alison/codeofalabama/1975/'

    def parse(self, response):
        print("________Processing URLs________")

        chapter_urls = response.xpath("/html//a/@href").extract()
        chapter_nums = response.xpath("/html//a/text()").extract()
        chapter_titles = response.xpath("/html/body/p/text()").extract()

        for chapter_url in enumerate(chapter_urls):
            # Get Chapter and URL information
            index = chapter_url[0]
            _chapter = chapter_nums[index] + ' ' + chapter_titles[index]

            absolute_url = self.BASE_URL + chapter_url[1]

            yield response.follow(absolute_url, callback=self.get_section_urls, meta={"Chapter": _chapter, "Url": absolute_url})

    def get_section_urls(self, response):
        # Passing spider to each section url and sending Chapter and URL item data with request
        chapter = response.meta['Chapter']
        chapter_url = response.meta['Url']

        section_urls = response.css('a::attr(href)').extract()
        urls = [self.BASE_URL+section_url for section_url in section_urls]

        return response.follow_all(urls, callback=self.parse_section, meta={"Chapter": chapter, "Url": chapter_url})

    def parse_section(self, response):
        item = LegisItem()

        item['Chapter'] = response.meta['Chapter']
        item['Url'] = response.meta['Url']

        item['Content'] = {

            'Section' : ' '.join(response.xpath("/html/body//u/text()").extract()),
            'Url' : ''.join(response.request.url),
            'Description': ' '.join(response.xpath("/html//h4/text()").extract()),
            'Language' : response.xpath("/html//p/text()").extract(),
            'Accts' : ' '.join(response.xpath("/html//i/text()").extract()),
        }

        return item
