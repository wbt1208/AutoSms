import requests
from collector.settings import *
import logging
url_detail = "https://www.yizhuan5.com/tools/gallery/article"
url_newlist = "http://www.yizhuan5.com/Mediabrary/data/HotMContent"

from dbcontext import HtmlSver


class ArticleCrawler:
    def __init__(self, conf):
        self.conf = conf["paramters"]
        self.list_re_body_bat = {
            paramters_map["source"]: source_map[self.conf["source"]],
            paramters_map["field"][0]: field_map[self.conf["field"]][0],
            paramters_map["field"][1]: field_map[self.conf["field"]][1],
            paramters_map["field"][2]: field_map[self.conf["field"]][2],

            paramters_map["keyword"][0]: "hmcttype" if self.conf["keyword"] == "" else "hmcttitle",
            paramters_map["keyword"][1]: "1" if self.conf["keyword"] == "" else "2",
            paramters_map["keyword"][2]: "1" if self.conf["keyword"] == "" else self.conf["keyword"],
        }
        self.update_headers()
        self.saver = HtmlSver()

    def update_article_list_re_body(self):
        date_1 = time.strftime('%Y-%m-%d 00:00', time.localtime(time.time() - 6 * 24 * 60 * 60))
        date_2 = time.strftime('%Y-%m-%d 00:00', time.localtime(time.time() + 24 * 60 * 60))
        list_body = {
            "PageIndex": "1",
            "PageSize": "15",
            "isppl": "true",
            "type": "1",
            "CID": "0",
            "OrderBy[0][Name]": "hmctdate",
            "OrderBy[0][OrderByType]": "2",
            "Where[0][Name]": "HMCTDate",
            "Where[0][Symbol]": "5",
            "Where[0][Value]": f"{date_1}",
            "Where[1][Name]": "HMCTDate",
            "Where[1][Symbol]": "6",
            "Where[1][Value]": f"{date_2}",
            "Where[2][Name]": "hmcttype",
            "Where[2][Symbol]": "1",
            "Where[2][Value]": "1"
        }
        list_body["PageIndex"] = str(self.page)
        list_body["Where[0][Value]"] = date_1
        list_body["Where[1][Value]"] = date_2
        if self.page <= 1:
            for k, v in self.list_re_body_bat.items():
                list_body[k] = v
        self.list_re_body = list_body

    def update_article_detail_body(self, detail_url):
        detail_body = {
            "hmcturl": "/Common/Tool/ToUrl?data=d8k6WnvzeGqeCN8bTwNz3ab6f63kBXYxxaErf4AnM%2fM%2bQCx8oROdvRoODhcyF%2f8VE1gRZt9%2fWV7E7WnnEJ%2bJYJNJe%2b9VI%2fYqzaYay%2beQDA00YthAzXe%2fDnczdBYyT7lPBUJt0ZtBNT3mLNNi9GErdTel9f%2bHlIrvDrA4lAQj6%2b4%3d"
        }
        detail_body["hmcturl"] = f"/Common/Tool/ToUrl?data={detail_url}"
        self.detail_body = detail_body

    def update_headers(self):
        self.headers = {
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

    def article_crawler_1zhuan(self):
        self.page = 0
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



