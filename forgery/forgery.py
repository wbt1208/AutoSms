from lxml import etree
from common.common import confutil
import os
import logging
import requests
from dbcontext.exception import *
import time
from collector.chrome import ChromeFectory
from selenium.webdriver.support.ui import Select


class Forgery():
    def __init__(self):
        self.html_path = confutil.get_html_path()
        self.forgery_html_path = confutil.get_forgery_html()
        self.forgery_word_path = confutil.get_forgery_word()
        if not os.path.exists(self.forgery_html_path):
            os.makedirs(self.forgery_html_path)
        if not os.path.exists(self.forgery_word_path):
            os.makedirs(self.forgery_word_path)

        if not os.path.exists(self.html_path):
            os.makedirs(self.html_path)

        self.forgery_api_1 = "http://192.168.1.4:8088/api"
        self.forgery_data_1 = 'title=&body={}'
        self.forgery_api_2 = "http://seowyc.com/seo/api/wyc.html"

    def run(self):
        while True:
            for filename in os.listdir(self.html_path):
                source_file = os.path.join(self.html_path, filename)
                dst_file = os.path.join(self.forgery_html_path, filename)
                if not os.path.exists(dst_file):
                    logging.info(f"> > >{source_file}> > >伪原创中")
                    with open(source_file, "r", encoding="utf-8") as fp:
                        html = fp.read()

                    html_tree = etree.HTML(html)
                    self.bianli(html_tree)
                    with open(dst_file, "w", encoding="utf-8") as fp:
                        fp.write(etree.tostring(html_tree, encoding="utf-8").decode())
                    logging.info(f"> > > {source_file} > > >伪原创成功")

    def bianli(self, html_tree):
        if html_tree is None:
            return
        for i in html_tree:
            forgery_text = self.callback(i.text)
            i.text = str(forgery_text)
            self.bianli(i)

    def callback(self, text):
        if not text:
            return ""
        logging.info(f"{text}")
        forgery_text = self.forgery_1(text)
        forgery_text = self.forgery_2(forgery_text)

        return forgery_text

    def forgery_1(self, text):
        try:
            logging.info(self.forgery_data_1)
            res = requests.post(self.forgery_api_1, data = self.forgery_data_1.format(text).\
                                encode(encoding='utf-8'))
        except Exception as e:
            raise ConnectException(*e.args)
        logging.info(f"{res.json()}")
        if res and res.status_code == 200:
            try:
                res_json = res.json()
                forgery_text = res_json["body"]
                if forgery_text:
                    forgery_text = forgery_text.replace("<p>", "").replace("</p>", "").replace(" ", "")
            except Exception as e:
                raise ReturnCodeException(*e.args)
            else:
                return forgery_text
        else:
            raise ReturnCodeException(res if not res else res.status_code)

    def forgery_2(self, text):
        chrome = ChromeFectory().get_chrome()
        chrome.set_page_load_timeout(5)
        try:
            chrome.get("http://seowyc.com/")
            time.sleep(1)
            chrome.execute_script('window.stop()')
            chrome.refresh()
            time.sleep(1)
            element = chrome.find_element_by_id("editor")
            element.send_keys("\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b"
                              "\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b"
                              "\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b"
                              "\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b")
            time.sleep(3)
            element.send_keys(text)
            time.sleep(2)
            select = Select(chrome.find_element_by_id("ratio"))
            select.select_by_index(3)
            time.sleep(1)
            chrome.find_element_by_xpath("//input[@value='生成伪原创']").click()
            time.sleep(3)
            chrome.implicitly_wait(10)
            print(element.text)
            # time.sleep(10)

        except Exception as e:
            logging.info(f"》》》seo伪原创失败 》》》{e.args}")
            return text
        else:
            return element.text
        finally:
            chrome.close()







