from parser_conf import conf
import os
from dbcontext.htow import HtmlToWord
class HtmlSver():
    def __init__(self):
        self.html_path = conf["html_path"]
        if not os.path.exists(self.html_path):
            os.makedirs(self.html_path)

    def save(self, file_name, body):
        file_name = os.path.join(self.html_path, file_name)
        with open(file_name, "w", encoding="utf-8") as fp:
            fp.write("<meta http-equiv=\"Content-Type\" content=\"text/html;charset=utf-8\">")
            fp.write(body)
