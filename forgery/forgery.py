from lxml import etree
from common.common import confutil,commonutil
import os
import logging
import requests
from requests.structures import CaseInsensitiveDict
import time
from collector.chrome import ChromeFectory


class Forgery():
    def __init__(self):
        self.chrome_fectory = ChromeFectory()
        self.chrome = self.chrome_fectory.get_chrome()
        self.chrome.minimize_window()
        self.chrome.set_page_load_timeout(5)
        try:
            self.chrome.get("http://seowyc.com/")
        except Exception as e:
            time.sleep(1)
            self.chrome.execute_script('window.stop()')
            self.chrome.refresh()
            time.sleep(1)
        self.html_path = confutil.get_html_path()
        self.forgery_html_path = confutil.get_forgery_html()
        self.forgery_word_path = confutil.get_forgery_word()
        if not os.path.exists(self.forgery_html_path):
            os.makedirs(self.forgery_html_path)
        if not os.path.exists(self.forgery_word_path):
            os.makedirs(self.forgery_word_path)

        if not os.path.exists(self.html_path):
            os.makedirs(self.html_path)

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
    @commonutil.retry
    def forgery_1(self, text):
        res = requests.post(self.forgery_api_1, data = self.forgery_data_1.format(text).\
                                encode(encoding='utf-8'))
        if res and res.status_code == 200:
            res_json = res.json()
            forgery_text = res_json["body"]
            if forgery_text:
                forgery_text = forgery_text.replace("<p>", "").replace("</p>", "").replace(" ", "")
                return forgery_text
        return ""
    @commonutil.retry
    def forgery_2(self, text):
        try:
            try:
                self.chrome.get("http://seowyc.com/")
            except Exception as e:
                self.chrome.execute_script("window.stop()")
            scripts_insert_html = "var insertDiv = document.getElementById('editor');insertDiv.innerHTML = '{}';"
            scripts_ratio = "var r = document.getElementById('ratio');r.selectedIndex={};"
            scripts_click = "convertWYC();"
            scripts_select_html = "var insertDiv = document.getElementById('editor');return insertDiv.innerHTML;"
            text = text.replace("'", "\\'").replace('\n', "\\n").replace("\"", "\\\"").\
                replace(" ", " ").replace("\t", "\\t")
            self.chrome.execute_script(
                scripts_insert_html.format(text)
            )
            time.sleep(5)
            self.chrome.execute_script(
                scripts_ratio.format(confutil.get_forgery_ratio())
            )
            time.sleep(5)
            self.chrome.execute_script(
                scripts_click
            )
            time.sleep(5)
            ret = self.chrome.execute_script(
                scripts_select_html
            )
            return ret
        except Exception as e:
            logging.info(f"》》》》》seo伪原创失败》》》》》》》》{e.args}")
            time.sleep(5)
            self.chrome.refresh()
            time.sleep(2)
            return text
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

    def __del__(self):
        self.chrome.close()







