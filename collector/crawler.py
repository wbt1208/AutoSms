from parser_conf import conf
from chrome import ChromeFectory
import time
import json
import logging
import sys
from xml import etree

class CrawlerFormatter:
    def __init__(self):
        self.browser = ChromeFectory(conf).get_chrome()
        self.auto_login = conf["auto_login"]
        self.login_wait_times = conf["login_wait_times"]
        self.browser.maximize_window()

    def __del__(self):
        self.browser.close()

class ArticleCrawler(CrawlerFormatter):
    def __init__(self):
        CrawlerFormatter.__init__(self)
        paramters = conf["paramters"]
        self.source = paramters["source"]
        self.field = paramters["field"]
        self.sort = paramters["sort"]
        self.type = paramters["type"]
        self.read_numbers = paramters["read_numbers"]
        self.time = paramters["time"]
        self.keyword = paramters["keyword"]



    def get_xpath(self):
        logging.info("解析xpath=========================")
        try:
            self.source_xpath = f"//div[@class='filter-row'][1]/div[@class='filter-content category-seconds-list clearfix']/span[contains(., '{self.source}')]"
            logging.info(self.source_xpath)
            self.browser.implicitly_wait(1)
            self.browser.find_element_by_xpath(self.source_xpath).click()

            self.field_xpath = f"//div[@class='filter-row'][2]/div[@class='filter-content category-seconds-list clearfix']/span[contains(., '{self.field}')]"
            logging.info(self.field_xpath)
            self.browser.implicitly_wait(1)
            self.browser.find_element_by_xpath(self.field_xpath).click()

            self.sort_xpath = f"//div[@class='filter-row'][3]//span[contains(., '{self.sort}')]"
            logging.info(self.sort_xpath)
            self.browser.implicitly_wait(1)
            self.browser.find_element_by_xpath(self.sort_xpath).click()

            self.type_xpath = f"//div[@class='filter-row'][4]//span[contains(., '{self.type}')]"
            logging.info(self.type_xpath)
            self.browser.implicitly_wait(1)
            self.browser.find_element_by_xpath(self.type_xpath).click()

            self.read_numbers_xpath = f"//div[@class='filter-row'][5]//span[contains(., '{self.read_numbers}')]"
            logging.info(self.read_numbers_xpath)
            self.browser.implicitly_wait(1)
            self.browser.find_element_by_xpath(self.read_numbers_xpath).click()

            self.time_xpath = f"//div[@class='filter-row'][6]//span[contains(., '{self.time}')]"
            logging.info(self.time_xpath)
            self.browser.implicitly_wait(1)
            self.browser.find_element_by_xpath(self.time_xpath).click()

            self.keyword_input_xpath = "//div[@class='filter-row'][7]//input[@placeholder='请输入关键词']"
            logging.info(self.keyword_input_xpath)
            self.browser.implicitly_wait(1)
            self.browser.find_element_by_xpath(self.keyword_input_xpath).send_keys(self.keyword["kw"])

            self.keyword_type_xpath = f"//div[@class='filter-row'][7]//span[contains(., '{self.keyword['kwtype']}')]"
            logging.info(self.keyword_type_xpath)
            self.browser.implicitly_wait(1)
            self.browser.find_element_by_xpath(self.keyword_type_xpath).click()

            self.keyword_mode_xpath = f"//div[@class='filter-row'][7]//label/span[contains(., '{self.keyword['kwmode']}')]"
            logging.info(self.keyword_mode_xpath)
            self.browser.implicitly_wait(1)
            self.browser.find_element_by_xpath(self.keyword_mode_xpath).click()

            self.keyword_click_xpath = "//div[@class='filter-row'][7]//button[contains(., '搜索')]"
            logging.info(self.keyword_click_xpath)
            self.browser.implicitly_wait(1)
            self.browser.find_element_by_xpath(self.keyword_click_xpath).click()

            self.title_xpath = ""
            self.

            logging.info("解析xpath=======================成功")
        except Exception as e:
            logging.error(f"解析xpath=====================失败 type = {e.__class__.__name__} info = {e.args[0]}")
            sys.exit(2)


    def article_crawler_1zhuan(self):
        # 易撰链接
        yizhuan_url = "http://www.yizhuan5.com/work.html#1-4"
        # 请求网页
        self.browser.get(yizhuan_url)

        # 添加cookie
        self.add_cookies(yizhuan_url, True)
        # 刷新
        self.browser.refresh()
        # 判断是否登录
        try:
            self.browser.find_element_by_xpath("//div[@class='form-item mobile']//input[@class='mat-input-element']")
            logging.error("易撰账户========================未登录")
            sys.exit(2)
        except Exception as e:
            logging.info(f"易撰账户=======================登录成功")

        self.get_xpath()

        # 最小化
        self.browser.minimize_window()

    def get_article(self):
        # 获取文章：标题，正文，来源，作者，领域，类型，时间，阅读，评论
        while True:
            for i in range(15):







        time.sleep(50)


        #
        # time.sleep(5)
        # self.browser.find_element_by_xpath("//div[@class='form-item mobile']//input[@class='mat-input-element']").click()
        # self.browser.find_element_by_xpath("//div[@class='form-item mobile']//input[@class='mat-input-element']").send_keys("17560318872")
        # time.sleep(5)

        # 登录

        #解析文章标题

        #解析富文本

        # return：
    def get_cookies(self, url):
        if self.auto_login:
            pass
            return
        else:
            time.sleep(self.login_wait_times)
            with open('cookies.json', "w+", encoding="utf-8") as fp:
                self.browser.implicitly_wait(5)
                json.dump(self.browser.get_cookies(), fp, indent=4)
    def add_cookies(self, url, init_cookies = True):
        if init_cookies:
            self.get_cookies(url)
        with open("cookies.json", "r", encoding="utf-8") as fp:
            logging.info("添加cookies=======================")
            try:
                cookies = json.load(fp)
                for cookie in cookies:
                    if 'expiry' in cookie:
                        cookie.pop('expiry')
                    self.browser.add_cookie(cookie)
                logging.info("添加cookies=======================成功")
            except Exception as e:
                logging.info(f"添加cookies=====================失败 type = {e.__class__.__name__} info = {e.args[0]}")




class ImageCrawler(CrawlerFormatter):
    def __init__(self):
        CrawlerFormatter.__init__(self)


