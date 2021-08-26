import requests
from collector.settings import *
import logging
url_detail = "https://www.yizhuan5.com/tools/gallery/article"
url_newlist = "http://www.yizhuan5.com/Mediabrary/data/HotMContent"

from dbcontext import HtmlSver


class ArticleCrawler:
    def __init__(self, conf):
        self.conf = conf
        self.paramters = conf["paramters"]
        self.saver = HtmlSver(conf)
        self.page = 0
        self.init_headers = {
            "Accept": "application/json, text/plain, */*",
            "Accept-Encoding": "gzip, deflate",
            "Accept-Language": "zh-CN,zh;q=0.9",
            "ajax": "true",
            "Connection": "keep-alive",
            "Content-Type": "application/x-www-form-urlencoded",
            "Cookie": self.conf["cookies"],
            "Host": "www.yizhuan5.com",
            "Origin": "http://www.yizhuan5.com",
            "Referer": "http://www.yizhuan5.com/work.html",
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36",
            "X-Requested-With": "XMLHttpRequest"
        }
        self.init_list_body =  {
            "PageIndex": "1",
            "PageSize": "15",
            "isppl": "true",
            "type": "1",
            "CID": "0",
            "OrderBy[0][Name]": "hmctdate",
            "OrderBy[0][OrderByType]": "2",
            "Where[0][Name]": "HMCTDate",
            "Where[0][Symbol]": "5",
            "Where[0][Value]": "",
            "Where[1][Name]": "HMCTDate",
            "Where[1][Symbol]": "6",
            "Where[1][Value]": "",
            "Where[2][Name]": "hmcttype",
            "Where[2][Symbol]": "1",
            "Where[2][Value]": "1"
        }                       
        self.init_detail_body = {
            "hmcturl": "/Common/Tool/ToUrl?"
        }
    def construct_headers(self):
        logging.info("构造请求头=======")
    def construct_list_body(self):
        logging.info("构造列表页请求体=======")
        # 只需要更新一次的
        if self.page <= 1:
            temp_body = {
                paramters_map["source"]: source_map[self.conf["source"]],
                paramters_map["field"][0]: field_map[self.conf["field"]][0],
                paramters_map["field"][1]: field_map[self.conf["field"]][1],
                paramters_map["field"][2]: field_map[self.conf["field"]][2],

                paramters_map["keyword"][0]: "hmcttype" if self.conf["keyword"] == "" else "hmcttitle",
                paramters_map["keyword"][1]: "1" if self.conf["keyword"] == "" else "2",
                paramters_map["keyword"][2]: "1" if self.conf["keyword"] == "" else self.conf["keyword"],
            }
            for k, v in temp.items():
                self.init_list_body[k] = v
        
        date_1 = time.strftime('%Y-%m-%d 00:00', time.localtime(time.time() - 6 * 24 * 60 * 60))
        date_2 = time.strftime('%Y-%m-%d 00:00', time.localtime(time.time() + 24 * 60 * 60))
        # 更新
        self.init_list_body["PageIndex"] = str(self.page)
        self.init_list_body["Where[0][Value]"] = date_1
        self.init_list_body["Where[1][Value]"] = date_2
    def construct_detail_body(self, url):
        self.init_detail_body["hmcturl"] = f"/Common/Tool/ToUrl?data={detail_url}"
    

    def article_crawler_1zhuan(self):
        res = None
        while True:
            self.page += 1
            self.update_article_list_re_body()
            try:
                res = requests.post(url=url_newlist, data=self.list_re_body, headers=self.headers)
            except Exception as e:
                pass

            if res and res.status_code == 200:
                article_json = res.json()
                article_json_lists = article_json["Data"]["List"]
                time.sleep(3)
                for article in article_json_lists:
                    hmcttitle = article["hmcttitle"]
                    logging.info(hmcttitle)
                    tags = article["tags"]
                    hmctdate = article["hmctdate"]
                    hmctsource = article["hmctsource"]
                    hmcturl = article["hmcturl"]
                    self.update_article_detail_body(hmcturl)
                    res_d = requests.post(url_detail, data=self.detail_body, headers=self.headers)
                    if res_d and res_d.status_code == 200:
                        detail_json = res_d.json()
                        hmctdeatil = detail_json["Data"]["content"]
                        # print(hmcttitle, hmctsource, hmctdate, tags, hmctdeatil)
                        file_name = f"{hmcttitle}_{hmctsource}_{hmctdate}.html"
                        self.saver.save(file_name, hmctdeatil)
                        time.sleep(int(self.conf["interval"]))



