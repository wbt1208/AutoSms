import os
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import sys
import logging
import platform


class ChromeFectory:
    def __init__(self, conf):
        self.path = conf["chrome_path"]
        self.driver_path = conf["chrome_driver_path"]
        self.auto_conf = conf["auto_conf_chrome"]
        self.takeover = conf["takeover"]
        self.simulate_mobile_phone = conf["simulate_mobile_phone"]
        self.options = webdriver.ChromeOptions()
        if self.simulate_mobile_phone:
            mobile_emulation = {
                "deviceName": "iPhone X"
            }
            experimental_option = ("mobileEmulation", mobile_emulation)
            self.options.add_experimental_option(*experimental_option)
        self.options.add_experimental_option('excludeSwitches', ['enable-automation', 'enable-logging'])
        if self.takeover:
            del self.options
            self.options = webdriver.ChromeOptions()
            self.options.add_experimental_option('debugerAddress', "127.0.0.1:54786")
        for arg in conf['chrome_options']:
            self.options.add_argument(arg)
        self.conf_chrome()

    def get_driver_version(self):
        info = os.popen(f'{self.driver_path} --version').read().strip()
        if info:
            logging.info(f"chromedriver version = {info}")
            return info.split()[1]
        return False

    def get_chrome_version(self):
        if platform.system().lower() == "windows":
            path = self.path.replace("\\", "\\\\")
            cmd = f"wmic datafile where name=\"{path}\" get version /value"
            info = os.popen(cmd).read().strip().split("=")[-1]
            if info:
                logging.info(f"chrome version = {info}")
                return info
            return False
        cmd = f"{self.path} --version"
        info = os.popen(cmd).read()
        if info:
            logging.info(f"chrome version = {info}")
            return info.split()[1]
        return False

    def match_version(self):
        self.driver_version = self.get_driver_version()
        self.chrome_version = self.get_chrome_version()
        if self.driver_version and self.chrome_version and self.driver_version == self.chrome_version:
            return True
        else:
            return False

    def conf_chrome(self):
        logging.info("配置chrome驱动=======================")
        if self.auto_conf:
            try:
                self.driver_path = ChromeDriverManager().install()
                logging.info("配置chrome驱动====================成功")
            except Exception as e:
                logging.error(f"配置chrome驱动=================失败 type = {e.__class__.__name__} info = {e.args[0]}")
                sys.exit(2)
        if not self.auto_conf:
            try:
                if self.match_version():
                    logging.info("配置chrome驱动====================成功")
                    self.options.binary_location = self.path
                else:
                    logging.info("配置chrome驱动====================失败")
                    sys.exit(2)
            except Exception as e:
                logging.error(f"配置chrome驱动=================失败 type = {e.__class__.__name__} info = {e.args[0]}")
                sys.exit(2)

    def get_chrome(self):
        return webdriver.Chrome(self.driver_path, chrome_options=self.options)
