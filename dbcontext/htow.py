import pypandoc
from parser_conf import conf
import time
import logging
import os

class HtmlToWord():
    def __init__(self):
        self.html_path = conf["html_path"]
        self.word_path = conf["word_path"]
        if not os.path.exists(self.html_path):
            os.makedirs(self.html_path)
        if not  os.path.exists(self.word_path):
            os.makedirs(self.word_path)

    def run(self):
        while True:
            for filename in os.listdir(self.html_path):
                source_file = os.path.join(self.html_path, filename)
                dst_file = os.path.join(self.word_path, filename.replace(".html", ".docx"))
                flag = False
                for dst_filename in os.listdir(self.word_path):

                    if self.get_title(filename) == self.get_title(dst_filename):
                        flag = True
                if not flag:
                    try:
                        pypandoc.convert_file(source_file, 'docx', outputfile = dst_file)
                    except Exception as e:
                        logging.error(f"html2word ===============   {e.args}")
            time.sleep(20)
    @staticmethod
    def get_title(filename):
        return filename.split("_")[0]


