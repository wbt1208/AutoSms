import os
from dbcontext.htow import HtmlToWord
import logging
class HtmlSver():
    def __init__(self, conf):
        self.html_path = conf["html_path"]
        if not os.path.exists(self.html_path):
            os.makedirs(self.html_path)

    def save(self, file_name, body):
        _file_name  = file_name.replace(" ","").replace("?", "").replace("？","").\
            replace("|", "").replace("、", "").replace("*","").replace(">", "").replace("<", "").\
            replace("\\", "").replace("/", "").replace("!", "").replace("@", "")
        try:
            __file_name = os.path.join(self.html_path, _file_name)
            __file_name = _file_name.replace("\\\\","/")
            with open(__file_name, "w+", encoding="utf-8") as fp:
                fp.write("<meta http-equiv=\"Content-Type\" content=\"text/html;charset=utf-8\">")
                fp.write(body)
                fp.flush()
                logging.info(f"{__file_name}=====下载成功")

        except Exception:
            __file_name = self.html_path + "/" + _file_name
            with open(__file_name, "w+", encoding="utf-8") as fp:
                fp.write("<meta http-equiv=\"Content-Type\" content=\"text/html;charset=utf-8\">")
                fp.write(body)
                fp.flush()
                logging.info(f"{__file_name}=====下载成功")

