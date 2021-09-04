import logging
import sys
import os
from collector import Getter
from dbcontext import HtmlToWord
from multiprocessing.dummy import Process
from forgery.forgery import Forgery
from common.common import confutil
from publisher.publisher import BaiPublisher
import traceback

def init_logging(filename, mode):
    logger = logging.getLogger('')
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
    filehandler = logging.FileHandler(
        filename = filename,
        mode = mode,
        encoding = "utf-8"
    )
    filehandler.setFormatter(formatter)
    logger.addHandler(filehandler)
    logger.setLevel(logging.INFO)

init_logging("autosms.log", "w")

def main():
    pgetter = forgeryhtml = ph2w = pbaipublisher =None
    if confutil.get_collector_status():
        getter = Getter()
        pgetter = Process(target=getter.run, args=())
    if confutil.get_forgery_status():
        forgery = Forgery()
        forgeryhtml = Process(target=forgery.run, args=())
    if confutil.get_html2word_status():
        h2w = HtmlToWord()
        ph2w = Process(target=h2w.run, args=())
    if confutil.get_publisher_status():
        baipublisher = BaiPublisher()
        pbaipublisher = Process(target=baipublisher.run, args=())

    if pgetter:
        logging.info("采集器启动》》》》》》》》》")
        pgetter.start()

    if forgeryhtml:
        logging.info("伪原创启动》》》》》》》》》")
        forgeryhtml.start()

    if ph2w:
        logging.info("html转word启动》》》》》》》")
        ph2w.start()
    if pbaipublisher:
        logging.info("发布器启动》》》》》》》》》")
        pbaipublisher.start()

    if pgetter:
        pgetter.join()
    if forgeryhtml:
        forgeryhtml.join()
    if ph2w:
        ph2w.join()
    if pbaipublisher:
        pbaipublisher.join()




if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        traceback.print_tb(e.__traceback__)
        logging.error(f"run error {e.args}")
        os.system("pause")
