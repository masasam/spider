import scrapy


class QiitaSpider(scrapy.Spider):
    name = 'qiita_spider'

    start_urls = ['http://qiita.com/advent-calendar/2015/categories/programming_languages']

    custom_settings = {
        "DOWNLOAD_DELAY": 1,
    }

    def parse(self, response):
        for href in response.css('.adventCalendarList .adventCalendarList_calendarTitle > a::attr(href)'):
            full_url = response.urljoin(href.extract())

            yield scrapy.Request(full_url, callback=self.parse_item)

    def parse_item(self, response):

        urls = []
        for href in response.css('.adventCalendarItem_entry > a::attr(href)'):
            full_url = response.urljoin(href.extract())
            urls.append(full_url)

        yield {
            'title': response.css('h1::text').extract(),
            'urls': urls,
        }
