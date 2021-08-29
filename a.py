import requests
from collector.chrome import ChromeFectory
ChromeFectory()

api = "http://seowyc.com/seo/api/wyc.html"
data = "content=我爱你中国&ratio=30"
headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36"
}
res = requests.post(api, headers = headers, data=data.encode("utf-8"))
print(res)