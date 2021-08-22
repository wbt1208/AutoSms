import logging
import sys
import json
import os

def set_default_conf():
    default_conf = {
        "chrome_path": "",
        "chrome_driver_path":"",
        "auto_conf_chrome": False,
        "takeover": False,
        "simulate_mobile_phone": False,
        'chrome_options': [
            "",
            ""
        ],
        "log_filename": "./autosms.log",
        "log_mode":"a+"
    }
    with open("./conf.json", "w+", encoding = "utf-8") as fp:
        json.dump(default_conf,fp, indent=4)

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