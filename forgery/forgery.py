from lxml import etree
from common.common import confutil
import os
import logging
import requests
from requests.structures import CaseInsensitiveDict
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
        self.chrome_fectory = ChromeFectory()
        self.forgery_api_1 = "http://192.168.1.5:8088/api"
        self.forgery_data_1 = 'title=&body={}'
        self.forgery_api_2 = "http://seowyc.com/seo/api/wyc.html"
        self.forgery_api_3 = "http://api-6.xiaofamao.com/api.php?json=0&v=1&key=ht721730467"

    def run(self):
        while True:
            for filename in os.listdir(self.html_path):
                source_file = os.path.join(self.html_path, filename)
                dst_file = os.path.join(self.forgery_html_path, filename)
                if not os.path.exists(dst_file):
                    logging.info(f"> > >{source_file}> > >伪原创中")
                    with open(source_file, "r", encoding="utf-8") as fp:
                        html = fp.read()
                    if "http://img.yizhuan5.com" not in html:
                        html = html.replace("//img.yizhuan5.com","http://img.yizhuan5.com")
                    html_tree = etree.HTML(html)
                    self.bianli(html_tree)
                    forgery_html = self.forgery_2(etree.tostring(html_tree, encoding="utf-8").decode())
                    with open(dst_file, "w", encoding="utf-8") as fp:
                        fp.write(forgery_html)
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
        forgery_text = self.forgery_1(text)
        # forgery_text = self.forgery_2(forgery_text)

        return forgery_text

    def forgery_1(self, text):
        try:
            res = requests.post(self.forgery_api_1, data = self.forgery_data_1.format(text).\
                                encode(encoding='utf-8'))
        except Exception as e:
            time.sleep(3)
            logging.warning("》》》》超人伪原创失败》》》正在重试")
            return self.forgery_1(text)
        if res and res.status_code == 200:
            try:
                res_json = res.json()
                forgery_text = res_json["body"]
                if forgery_text:
                    forgery_text = forgery_text.replace("<p>", "").replace("</p>", "").replace(" ", "")
            except Exception as e:
                logging.warning("》》》》超人伪原创失败》》》正在重试")
                return self.forgery_1(text)
            else:
                return forgery_text
        else:
            logging.warning("》》》》超人伪原创失败》》》正在重试")
            return self.forgery_1(text)

    def forgery_2(self, text):
        chrome = self.chrome_fectory.get_chrome()
        chrome.minimize_window()
        chrome.set_page_load_timeout(5)
        try:
            try:
                chrome.get("http://seowyc.com/")
            except Exception as e:
                time.sleep(1)
                chrome.execute_script('window.stop()')
                chrome.refresh()
            time.sleep(1)
            text.replace('\'',"").replace('\n', "")
            scrits = "var insertDiv = document.getElementById('editor');insertDiv.innerHTML = '{}'"
            # chrome.execute_script(scrits.format(''))
            # for i in range(50):
                # element.send_keys("\b\b")

                # chrome.implicitly_wait(10)
            # for t in text:
            #     element.send_keys(t)
            #     chrome.implicitly_wait(10)
            chrome.implicitly_wait(10)
            chrome.execute_script(scrits.format(text))
            time.sleep(2)
            try:
                chrome.execute_script("var r = document.getElementById('ratio');r.selectedIndex={};".format(confutil.get_forgery_ratio()))
                time.sleep(2)
            except:
                select = Select(chrome.find_element_by_id("ratio"))
                logging.warning(confutil.get_forgery_ratio())
                select.select_by_index(confutil.get_forgery_ratio())
                time.sleep(1)
            chrome.find_element_by_xpath("//input[@value='生成伪原创']").click()
            time.sleep(10)
            chrome.implicitly_wait(10)
            # print(element.text)
            # time.sleep(10)

        except Exception as e:
            logging.info(f"》》》》》seo伪原创失败  重试》》》{e.args}")
            time.sleep(5)
            chrome.close()
            time.sleep(2)
            return self.forgery_2(text)
        else:
            try:
                element = chrome.find_element_by_id("editor")
            except:
                time.sleep(5)
                chrome.close()
                time.sleep(2)
                logging.info(f"》》》》》seo伪原创失败  重试》》》{e.args}")
                return self.forgery_2(text)
            else:
                chrome.close()
                return element.get_attribute("outerHTML")

    def forgery_3(self, text):
        headers = CaseInsensitiveDict()
        headers["Accept"] = "application/json"
        headers["Content-Type"] = "application/x-www-form-urlencoded"
        data = "wenzhang={}"
        try:
            resp = requests.post(self.forgery_api_3, headers=headers, data=data.format(text).encode(encoding='utf-8'))
        except Exception as e:
            logging.error(e.args)
        else:
            if resp and resp.status_code == 200:
                return resp.text







