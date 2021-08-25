import logging
import sys
import json
import os


def set_default_conf():
    default_conf = {
        "autosms_mode": 1,
        "paramters": {
            "source": "百家号",
            "field": "全部",
            "keyword": "周",
            "interval": "20",
            "cookies": "UM_distinctid=17b694205d8261-0b9e0ad739305c-35617403-13c680-17b694205d934f; Identification=13353936525; PwdToken=44a072122c0c4650d9c39e7b8ca20660; mySpread=36HWDDZJ; Hm_lvt_119d728e13405b1761bac1057994ec52=1629558541,1629826666; Token=d6040574-6c8a-4bac-b1a9-4aabd2cabac3; WxScanOpenId=b2lDZTEwbldfWGtuaHZUM1pZOS14c212N0RqOA; ct=d6040574-6c8a-4bac-b1a9-4aabd2cabac3_1629895511448; CNZZDATA1278145158=2113046919-1629553933-null%7C1629895454; Hm_lpvt_119d728e13405b1761bac1057994ec52=1629895537; ckt=1629895550"
        },
        "html_path": "html",
        "word_path": "wold",
        "mysqldb": {
            "host": "",
            "port": "",
            "user": "",
            "passwd": "",
            "dbname": ""
        },
        "log_filename": "./autosms.log",
        "log_mode": "a+"
    }
    with open("./conf.json", "w+", encoding="utf-8") as fp:
        json.dump(default_conf, fp, indent=4)


def get_conf():
    logging.info("加载配置文件=====================")
    if not os.path.exists("./conf.json"):
        logging.warning("加载配置文件==============失败  缺少conf.json文件")
        set_default_conf()
    try:
        with open("./conf.json", "r", encoding="utf-8") as fp:
            conf = json.load(fp)
            for k, v in conf.items():
                logging.info(f"{k} = {v}")
            logging.info("加载配置文件===================成功")
            return conf
    except Exception as e:
        logging.error(f"加载配置文件==============失败  {e.args[-1]}")
        sys.exit(2)


logger = logging.getLogger()
for handler in logger.handlers:
    logger.removeHandler(handler)
stdhandler = logging.StreamHandler(sys.stdout)
formatter = logging.Formatter(
    fmt="[%(asctime)s.%(msecs)03d]-[%(process)d]-[%(levelname)s]: %(message)s(%(filename)s:%(lineno)d)",
    datefmt='%Y-%m-%d,%H:%M:%S'
)
stdhandler.setFormatter(formatter)
stdhandler.setLevel(logging.INFO)
logger.addHandler(stdhandler)
logger.setLevel(logging.INFO)
conf = get_conf()
