# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals

# useful for handling different item types with a single interface
from itemadapter import is_item, ItemAdapter
from scrapy.http import HtmlResponse
from selenium import webdriver
import time


class SeleniumMiddleware(object):
    
    def process_request(self, request, spider):
        # 获取正在爬取的页面
        url = request.url
        # 使用Chrom浏览请求
        browser = webdriver.Chrome()
        browser.get(url)
        time.sleep(5)
        # 获取最终的html代码
        html = browser.page_source
        browser.close()
        # 使用HTML代码构造HtmlResponse并返回
        # 因为使用的是HtmlResponse对象，所以原来的request就会被忽略
        # 这个HtmlResponse对象会被发送给Spider来解析，所以Response拿到的就是selenium渲染后的结果了

        return HtmlResponse(url=request.url,
                            body=html,
                            request=request,
                            encoding='utf-8',
                            status=200)
