import logging
import re
from scrapy import Request, Spider
from gerapy_selenium import SeleniumRequest
from scrapyseleniumdemo.items import BookItem

logger = logging.getLogger(__name__)


class BookSpider(Spider):
    name = 'book'
    allowed_domains = ['spa5.scrape.center']
    base_url = 'https://spa5.scrape.center'

    # 构造列表第一页的url，然后将其构造成Request对象并返回，回调parse_index方法
    def start_requests(self):
        """
        first page
        :return:
        """
        start_url = f'{self.base_url}/page/1'
        logger.info('crawling %s', start_url)
        yield SeleniumRequest(start_url, callback=self.parse_index, wait_for='.item .name')

    # 实现列表页的解析，得到详情页的url,同时解析下一页的url
    def parse_index(self, response):
        """
        extract books and get next page
        :param response:
        :return:
        """
        # 解析每一本书的详情url,构造新的Request并返回，回调方法设置为parse_detail，优先级设置为2
        items = response.css('.item')
        for item in items:
            href = item.css('.top a::attr(href)').extract_first()
            detail_url = response.urljoin(href)
            yield SeleniumRequest(detail_url, callback=self.parse_detail, priority=2, wait_for='.item .name')

        # next page
        # 获取当前列表页码，然后将其加1后构造下一页的url,构造新的Request并返回，回调方法设置为parse_index
        match = re.search(r'page/(\d+)', response.url)
        if not match:
            return
        page = int(match.group(1)) + 1
        next_url = f'{self.base_url}/page/{page}'
        yield SeleniumRequest(next_url, callback=self.parse_index, wait_for='.item .name')

    # 解析详情页提取最终结果，构造BookItem并返回
    def parse_detail(self, response):
        """
        process detail info of book
        :param response:
        :return:
        """
        name = response.css('.name::text').extract_first()
        tags = response.css('.tags button span::text').extract()
        score = response.css('.score::text').extract_first()
        price = response.css('.price span::text').extract_first()
        cover = response.css('.cover::attr(src)').extract_first()
        tags = [tag.strip() for tag in tags] if tags else []
        score = score.strip() if score else None
        item = BookItem(name=name, tags=tags, score=score,
                        price=price, cover=cover)
        yield item
