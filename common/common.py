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

# from ctypes import windll
# import time
# import win32file
# from win32file import *
#
# def is_open(filename):
#     try:
#         # 首先获得句柄
#         vHandle = win32file.CreateFile(filename, GENERIC_READ, 0, None, OPEN_EXISTING, FILE_ATTRIBUTE_NORMAL, None)
#         # 判断句柄是否等于INVALID_HANDLE_VALUE
#         if int(vHandle) == INVALID_HANDLE_VALUE:
#             win32file.CloseHandle(vHandle)
#             logging.info(f"{filename} is already open")
#             return True  # file is already open
#         else:
#             return False
#     except Exception as e:
#         return True





class ConfUtil(ConfUtilFornatter):
    def __init__(self):
        self.get_conf()

    @staticmethod
    def set_default_conf():
        default_conf = {
            "autosms_mode": 1,
            "paramters": {
                "source": "百家号",
                "field": "全部",
                "keyword": "",
                "interval": "20",
                "cookies": "UM_distinctid=17b694205d8261-0b9e0ad739305c-35617403-13c680-17b694205d934f; Identification=13353936525; PwdToken=44a072122c0c4650d9c39e7b8ca20660; mySpread=36HWDDZJ; Hm_lvt_119d728e13405b1761bac1057994ec52=1629558541,1629826666; Token=d6040574-6c8a-4bac-b1a9-4aabd2cabac3; WxScanOpenId=b2lDZTEwbldfWGtuaHZUM1pZOS14c212N0RqOA; ct=d6040574-6c8a-4bac-b1a9-4aabd2cabac3_1629895511448; CNZZDATA1278145158=2113046919-1629553933-null%7C1629895454; Hm_lpvt_119d728e13405b1761bac1057994ec52=1629895537; ckt=1629895550"
            },
            "html_path": ".\\html",
            "word_path": ".\\wold",
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
        return self.conf["interval"]
    def get_html_path(self):
        return self.conf["html_path"]
    def get_word_path(self):
        return self.conf["word_path"]

confutil = ConfUtil()



