import logging
import sys
from parser_conf import conf

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





if __name__ == '__main__':
    init_logging(conf["log_filename"], conf["log_mode"])