import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from scrapy.selector import Selector
import pandas as pd
import time

import logging
from logging import config
from conf import *
from pathlib import Path

config.dictConfig(LOGGING)
logger = logging.getLogger('main')


class NewsScrapeSpider(scrapy.Spider):
    name = 'news_spider'
    start_urls = ['https://finance.yahoo.com/news/']
    custom_settings = {
        'FEED_URI': 'finance_news.json',
        'FEED_FORMAT': 'json',
        'FEED_EXPORT_ENCODING': 'utf-8'
    }

    def parse(self, response, **kwargs):
        # initiating chrome driver
        options = Options()
        chrome_user_data_dir = Path(BASE_DIR, 'user_data_dir')
        # comment if you want to see the browser window otherwise it will be headless
        options.add_argument("--headless")
        options.add_argument('--log-level=3')
        options.add_argument("--start-maximized")
        # setting a user-data-dir to keep the cache and other states
        options.add_argument(f"user-data-dir={chrome_user_data_dir}")
        chrome_path = Path(BASE_DIR, 'drivers/chromedriver.exe')
        driver = webdriver.Chrome(executable_path=chrome_path, options=options)
        logger.info('selenium driver initiated.')
        logger.info(f'scroll pause time: {SCROLL_PAUSE_TIME}')
        logger.info(f'getting into the link: {self.start_urls[0]}')
        driver.get(self.start_urls[0])
        time.sleep(SCROLL_PAUSE_TIME)
        # the site has a kind of infinite scrolling feature.
        # so it need to be tweaked to scroll down with the power of selenium
        last_link = None
        while True:
            logger.info('sending keys for scrolling')
            driver.find_element(By.XPATH, '//body').send_keys(Keys.END)
            # giving required time to load content after scrolling
            time.sleep(SCROLL_PAUSE_TIME)
            new_last_link = driver.find_elements(By.XPATH, '//div[@class="Cf"]//a')[-1].get_attribute('href')
            logger.info(f'new last link: {new_last_link}')
            logger.info(f'last link: {last_link}')
            if new_last_link == last_link:
                logger.info('bottom of the page arrived')
                break
            else:
                last_link = new_last_link
        resp = Selector(text=driver.page_source)
        logger.info('final response taken')
        links = resp.xpath('//div[@class="Cf"]//a/@href').getall()
        for link in links:
            # parsing individual links
            yield response.follow(link, callback=self.parse_news, cb_kwargs={'url': response.urljoin(link)})

    def parse_news(self, response, **kwargs):
        link = kwargs['url']
        logger.info(f'crawling news from: {link}')
        title = response.xpath('//h1[@data-test-locator="headline"]/text()').get()
        logger.info(f'news title: {title}')
        author = response.xpath('//span[@class="caas-author-byline-collapse"]/text()').get()
        post_timestamp = response.xpath('//div[@class="caas-attr-time-style"]//time/text()').get()
        post_minute_read = response.xpath('//span[@class="caas-attr-mins-read"]/text()').get()
        post_text = '\n'.join(response.xpath('//div[@class="caas-body"]//p/text()').getall())

        logger.info(f'crawling done for: {link}')
        data_dict = {
            'link': link,
            'title': title,
            'author': author,
            'post_timestamp': post_timestamp,
            'post_minute_read': post_minute_read,
            'post_text': post_text,
        }
        df = pd.DataFrame(data_dict, index=[0])
        df['post_timestamp'] = pd.to_datetime(df['post_timestamp'], format='%B %d, %Y, %I:%M %p', errors='coerce')
        yield from df.to_dict(orient='records')


settings = get_project_settings()
settings.update({
    'LOG_LEVEL': 'ERROR',
    'LOG_FORMAT': '"[%(asctime)s] : %(levelname)s : [%(module)s:%(lineno)s] : [%(funcName)s] : %(message)s"',
    'LOG_FILE': 'crawler_error.log'
})
process = CrawlerProcess(settings)
process.crawl(NewsScrapeSpider)
process.start()
