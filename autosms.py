import logging
import sys
import os
from collector import Getter
from dbcontext import HtmlToWord
from multiprocessing import Process

def init_logging(filename, mode):
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
    filehandler = logging.FileHandler(
        filename = filename,
        mode = mode,
        encoding = "utf-8"
    )
    filehandler.setFormatter(formatter)
    logger.addHandler(filehandler)
    logger.setLevel(logging.INFO)

def main():
    getter = Getter()
    h2w = HtmlToWord()
    pgetter = Process(target=getter.run, args = ())
    ph2w = Process(target=h2w.run, args=())
    pgetter.start()
    ph2w.start()
    pgetter.join()
    ph2w.join()



if __name__ == '__main__':
    init_logging("./autosms.log", "w+")
    try:
        main()
    except Exception as e:
        logging.info(f"run error {e.args}")
        os.system("pause")
