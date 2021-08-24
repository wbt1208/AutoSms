import requests
import time
from
from settings import *
import json
url_detail = "https://www.yizhuan5.com/tools/gallery/article"
url_newlist = "http://www.yizhuan5.com/Mediabrary/data/HotMContent"
headers = {
    "Accept": "application/json, text/plain, */*",
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "zh-CN,zh;q=0.9",
    "ajax": "true",
    "Connection": "keep-alive",
    "Content-Type": "application/x-www-form-urlencoded",
    "Cookie": "UM_distinctid=17b694205d8261-0b9e0ad739305c-35617403-13c680-17b694205d934f; Hm_lvt_119d728e13405b1761bac1057994ec52=1629558541; WxScanOpenId=b2lDZTEwbldfWGtuaHZUM1pZOS14c212N0RqOA; WxBindMobileId=oiCe10nW_XknhvT3ZY9-xsmv7Dj8; href=http%3A%2F%2Fwww.yizhuan5.com%2F%3Frd%3D1; CNZZDATA1278145158=2113046919-1629553933-null%7C1629811359; Identification=13353936525; PwdToken=44a072122c0c4650d9c39e7b8ca20660; Token=dce7749b-c45e-4242-985e-7e914b899c7a; ct=dce7749b-c45e-4242-985e-7e914b899c7a_1629814954263; mySpread=36HWDDZJ; Hm_lpvt_119d728e13405b1761bac1057994ec52=1629814955; ckt=1629814971",
    "Host": "www.yizhuan5.com",
    "Origin": "http://www.yizhuan5.com",
    "Referer": "http://www.yizhuan5.com/work.html",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36",
    "X-Requested-With": "XMLHttpRequest"
}
data_detail = {
    "hmcturl": "/Common/Tool/ToUrl?data=d8k6WnvzeGqeCN8bTwNz3ab6f63kBXYxxaErf4AnM%2fM%2bQCx8oROdvRoODhcyF%2f8VE1gRZt9%2fWV7E7WnnEJ%2bJYJNJe%2b9VI%2fYqzaYay%2beQDA00YthAzXe%2fDnczdBYyT7lPBUJt0ZtBNT3mLNNi9GErdTel9f%2bHlIrvDrA4lAQj6%2b4%3d"
}
data_list = {
"PageIndex": "2",
"PageSize": "15",
"isppl": "true",
"type": "1",
"CID": "0",
"OrderBy[0][Name]": "hmctamout",
"OrderBy[0][OrderByType]": "2",
"Where[0][Name]": "HMCTDate",
"Where[0][Symbol]": "5",
"Where[0][Value]": "2021-08-18 00:00",
"Where[1][Name]": "HMCTDate",
"Where[1][Symbol]": "6",
"Where[1][Value]": "2021-08-25 00:00",
"Where[2][Name]": "hmcttype",
"Where[2][Symbol]": "1",
"Where[2][Value]": "1"
}
class ArticleCrawler:
    def __init__(self, conf):
        pass

    def article_crawler_1zhuan(self):
        page = 1
        res = None
        data_list["PageIndex"] = str(page)
        while True:
            try:
                res = requests.post(url = url_newlist, data = data_list, headers = headers)
            except Exception as e:
                pass
            if res and res.status_code == 200:
                article_json = res.json()
                article_json_lists = article_json["Data"]["List"]
                time.sleep(3)
                for article in article_json_lists:
                    hmcttitle = article["hmcttitle"]
                    tags = article["tags"]
                    hmctdate = article["hmctdate"]
                    hmctsource = article["hmctsource"]
                    hmcturl = article["hmcturl"]
                    data_detail["hmcturl"] = "/Common/Tool/ToUrl?data=" + hmcturl
                    res_d = requests.post(url_detail, data=data_detail, headers = headers)
                    if res_d and res_d.status_code == 200:
                        detail_json = res_d.json()
                        print(detail_json)
                        hmctdeatil = detail_json["Data"]["content"]
                        print(hmcttitle, hmctsource, hmctdate, tags, hmctdeatil)
                        time.sleep(10)






ArticleCrawler().article_crawler_1zhuan()