import json
import logging
import os


class ConfUtilFornatter(object):
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, '_singleton'):
            cls._singleton = object.__new__(cls)
            return cls._singleton
        else:
            return cls._singleton


class ConfUtil(ConfUtilFornatter):
    def __init__(self):
        self.get_conf()

    @staticmethod
    def set_default_conf():
        default_conf = {
            "autosms_mode": 1,
            "paramters": {
                "source": "百家号",
                "field": "历史",
                "start_date": "2020-06-16",
                "end_date": "2021-06-16",
                "keyword": "二战"
            },
            "interval": "20",
            "cookies": "UM_distinctid=17b694205d8261-0b9e0ad739305c-35617403-13c680-17b694205d934f; Identification=13353936525; PwdToken=44a072122c0c4650d9c39e7b8ca20660; mySpread=36HWDDZJ; Hm_lvt_119d728e13405b1761bac1057994ec52=1629558541,1629826666; WxScanOpenId=b2lDZTEwbldfWGtuaHZUM1pZOS14c212N0RqOA; Token=2d34d0a9-03ef-4d58-bfeb-4751571ce368; scene_id=69791513; ct=2d34d0a9-03ef-4d58-bfeb-4751571ce368_1630071081449; CNZZDATA1278145158=2113046919-1629553933-null%7C1630067977; Hm_lpvt_119d728e13405b1761bac1057994ec52=1630071083; ckt=1630071951",
            "html_path": "html",
            "word_path": "wold",
            "forgery_html_path": "forgery_html",
            "forgery_word_path": "forgery_word",
            "forgery_ratio": "20",
            "mysqldb": {
                "host": "",
                "port": "",
                "user": "",
                "passwd": "",
                "dbname": ""
            }
        }
        with open("./conf.json", "w+", encoding="utf-8") as fp:
            json.dump(default_conf, fp, indent=4)

    def get_conf(self):
        logging.info("加载配置文件=====================")
        if not os.path.exists("./conf.json"):
            logging.warning("加载配置文件==============失败  缺少conf.json文件")
            self.set_default_conf()
        try:
            with open("./conf.json", "r", encoding="utf-8") as fp:
                self.conf = json.load(fp)
        except Exception as e:
            logging.error(f"加载配置文件==============失败  {e.args[-1]}")
            os.system("pause")

    def get_cookies(self):
        return self.conf["cookies"]

    def get_paramters(self):
        return self.conf["paramters"]

    def get_interval(self):
        if int(self.conf["interval"]) < 20:
            logging.warning("》》》》》》》采集间隔不得低于20s》》》》》》》")
            self.conf["interval"] = "20"
        return self.conf["interval"]

    def get_html_path(self):
        return self.conf["html_path"]

    def get_word_path(self):
        return self.conf["word_path"]

    def get_start_date(self):
        return self.conf["paramters"]["start_date"] + " 00:00"

    def get_end_date(self):
        return self.conf["paramters"]["end_date"] + " 00:00"

    def get_forgery_html(self):
        return self.conf["forgery_html_path"]

    def get_forgery_word(self):
        return self.conf["forgery_word_path"]

    def get_forgery_ratio(self):
        return self.conf["forgery_ratio"]
    def get_app_id(self):
        return self.conf["app_id"]
    def get_app_token(self):
        return self.conf["app_token"]
    def get_collector_status(self):
        return "enable" in self.conf["collector_status"]
    def get_html2word_status(self):
        return "enable" in self.conf["html2word_status"]
    def get_forgery_status(self):
        return "enable" in self.conf["forgery_status"]
    def get_publisher_status(self):
        return "enable" in self.conf["publisher_status"]

    # import win32file
    # def is_used(filename):
    #     try:
    #         vHandel = win32file.CreateFile(filename, win32file.GENERIC_READ, 0, None, win32file.OPEN_EXISTING,
    #                                        win32file.FILE_ATTRIBUTE_NORMAL, None)
    #     except Exception as e:
    #         if "正在使用" in e.args[-1]:
    #         return True
    #     else:
    #         raise FileExistsError(*e.args)
    #     else:
    #         win32file.CloseHandle(vHandel)
    #         return False


confutil = ConfUtil()
