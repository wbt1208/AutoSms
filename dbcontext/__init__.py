import os
from dbcontext.htow import HtmlToWord
import logging
from common.common import confutil
class HtmlSver():
    def __init__(self):
        self.html_path = confutil.get_html_path()
        if not os.path.exists(self.html_path):
            os.makedirs(self.html_path)

    def save(self, file_name, title, body):
        file_name  = file_name.replace(" ","").replace("?", "").replace("？","").\
            replace("|", "").replace("、", "").replace("*","").replace(">", "").replace("<", "").\
            replace("\\", "").replace("/", "").replace("!", "").replace("@", "").replace("！","").replace(":", "").\
            replace("：", "")
        try:
            file_name = os.path.join(self.html_path, file_name)
            if body.__sizeof__() > 200:
                with open(file_name, "w+", encoding="utf-8") as fp:
                    fp.write("<meta http-equiv=\"Content-Type\" content=\"text/html;charset=utf-8\">")
                    # fp.write(f"<h1><strong>{title}</strong></h1>")
                    fp.write(body)
                    fp.flush()
                    logging.info(f"{file_name}=====下载成功")
            else:
                logging.info(f"{file_name}====过小===忽略")

        except Exception:
            logging.info(f"{file_name}=====下载失败")

