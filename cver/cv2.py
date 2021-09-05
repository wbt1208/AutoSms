
import requests
import os
import re

url = "http://img.yizhuan5.com/common/tool/yzimg?o=2&data=5fa3ce673b52318617811be8e929ed0a55d001956ebee5364deda852fbda2033dcd7c2089a582a0485025a844d4f7c27a89aabe51b5d7b91dd967c3e11df93953bab9074e70463ddf5c5535f6723af4ba97a81539c1a030b52bd46dab45c13e9ef047b0699d20548104e671ff4bb5ce28c0b58a449b722c4a37996ee8ec79afcb0225f887e6fdd39"
class Cv2:
    def __init__(self):
        self.img_re = re.compile("<img src=\"(.*?)\">")
        self.cv2_html = "cv2_temp"
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Linux; Android 6.0.1; Moto G (4)) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Mobile Safari/537.36"
        }
        if not os.path.exists(self.cv2_html):
            os.makedirs(self.cv2_html)
    def run(self):
        fp = open("女子如何增加魅力，清朝赛金花有三个绝招，可以给当代人提供借鉴_历史店_2020-10-22082439.html", "r", encoding="utf-8")
        img_urls = self.img_re.findall(fp.read())
        for img_url in img_urls:
            img_url = img_url.replace('amp;', '')
            res = requests.get(img_url, headers = self.headers)
            if res and res.status_code == 200:
                with open(os.path.join(self.cv2_html, img_url.split("=")[-1][10:50] + ".png"), "wb+") as img_fp:
                    img_fp.write(res.content)
            # break
        fp.close()
cv2 = Cv2()
cv2.run()