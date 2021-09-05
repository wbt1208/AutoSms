from requests import Session
import logging
from common.common import confutil
from .exception import *
# import json
import os
import time
exception_code = {
    "0": "成功",
    "2": "参数错误",
    "4": "数据库错误",
    "5": "数据库错误",
    "10002": "无权限调用相关接口",
    "10003": "数据库错误",
    "10005": "百家号内部服务异常",
    "10009": "非作者文章",
    "27012": "文章修改次数达到上限",
    "301001": "无有效数据",
    "301002": "今日上传图片次数耗尽",
    "301003": "图片重复入库",
    "301004": "要删除的图片不存在",
    "300016": "目前只有图文类型支持修改",
    "60001001":	"授权校验失败",
    "60001003":	"撤回或修改时文章状态错误",
    "60000005":	"帐号未审核通过或在禁言期",
    "60000006":	"百家号内部服务异常",
    "60000009":	"帐号不存在",
    "60000020":	"百家号内部服务异常",
    "60001008":	"当天发文篇数校验失败",
    "60001009":	"发文篇数用尽",
    "80000107":	"文章不存在",
    "800000201": "文章状态异常"
}
class BaiPublisher:
    picture_text_api = "https://baijiahao.baidu.com/builderinner/open/resource/article/publish"
    gallery_api = "https://baijiahao.baidu.com/builderinner/open/resource/article/gallery"
    video_api = "https://baijiahao.baidu.com/builderinner/open/resource/video/publish"
    withdraw_api = "https://baijiahao.baidu.com/builderinner/open/resource/article/withdraw"
    republish_api = "https://baijiahao.baidu.com/builderinner/open/resource/article/republish"
    query_status_api = "https://baijiahao.baidu.com/builderinner/open/resource/query/status"
    query_list_api = "https://baijiahao.baidu.com/builderinner/open/resource/query/articleListall"
    def __init__(self):
        self.session = Session()
        self.session.headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36"
        }
        self.app_id = confutil.get_app_id()
        self.app_token = confutil.get_app_token()
        self.publish_picture_text_data = dict()
        self.query_status_data = dict()
        self.query_list_data = dict()
        self.publisher_html_path = "publish_html"
        if not os.path.exists(self.publisher_html_path):
            os.makedirs(self.publisher_html_path)
        self.published_html_path = "temp_ped"
        if not os.path.exists(self.published_html_path):
            os.makedirs(self.published_html_path)
    def run(self):
        while True:
            for filename in os.listdir(self.publisher_html_path):
                source_file = os.path.join(self.publisher_html_path, filename)
                dst_file = os.path.join(self.published_html_path, filename)
                if not os.path.exists(dst_file):
                    with open(source_file, "r", encoding="utf-8") as fp:
                        content = fp.read()
                        with open(dst_file, "w", encoding="utf-8") as fpd:
                            fpd.write(content)
                        if content.__sizeof__() < 200:
                            logging.info(f"$$$$ {filename} 过小 $$$$ 忽略")
                            continue
                        self.publish_picture_text(
                            title=filename.replace(".html",""),
                            content=content,
                            origin_url=f"http://baijiahao.baidu.com/s?id={hash(filename)}",
                            cover_images = "",
                            is_original=1,
                            is_split_article='',
                            video_title='',
                            video_cover_images=''
                        )
            time.sleep(int(confutil.get_interval()))

    def publish_picture_text(self, title, content, origin_url, cover_images,
                             is_original, is_split_article, video_title, video_cover_images):

        self.publish_picture_text_data["app_id"] = self.app_id
        self.publish_picture_text_data["app_token"] = self.app_token
        self.publish_picture_text_data["title"] = title
        self.publish_picture_text_data["content"] = content
        self.publish_picture_text_data["origin_url"] = origin_url
        self.publish_picture_text_data["cover_images"] = cover_images
        self.publish_picture_text_data["is_original"] = is_original
        print(self.publish_picture_text_data)
        # self.publish_picture_text_data["is_split_article"] = is_split_article
        # self.publish_picture_text_data["video_title"] = video_title
        # self.publish_picture_text_data["video_cover_images"] = video_cover_images
        try:
            res = self.session.post(self.picture_text_api, data=self.publish_picture_text_data)
        except Exception as e:
            logging.error("publisher connect error ####")
            raise ConnectException(*e.args)
        else:
            if res and res.status_code == 200:
                res_json = res.json()
                try:
                    errno = res_json["errno"]
                    errmsg = res_json["errmsg"]
                    data = res_json["data"]
                    print(errno, errmsg, data)
                except Exception as e:
                    logging.error("publisher return error #### ")
                    raise ReturnCodeException(*e.args)
                else:
                    if errno == 0:
                        logging.info(f"publish #### {title} success #### {errmsg} {data}####")
                    else:
                        logging.error(f"publish #### {title} filed #### {errmsg} {data} ####")
    def query_status(self, article_id):
        self.query_status_data["app_id"] = self.app_id
        self.query_status_data["app_token"] = self.app_token
        self.query_status_data["article_id"] = article_id
        res = self.session.post(self.query_status_api, data=self.query_status_data)
        print(res.json())
    def query_list(self, start_time = None, end_time = None):
        self.query_list_data["app_id"] = self.app_id
        self.query_list_data["app_token"] = self.app_token
        if start_time:
            self.query_list_data["start_time"] = start_time
        if end_time:
            self.query_list_data["end_time"] = end_time
        res = self.session.post(self.query_list_api, data=self.query_list_data)
        print(res.json())




