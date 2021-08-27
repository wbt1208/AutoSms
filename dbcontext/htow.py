import pypandoc
import time
import logging
import os
from common.common import confutil
class HtmlToWord():
    def __init__(self):
        self.html_path = confutil.get_html_path()
        self.word_path = confutil.get_word_path()
        self.forgery_path = confutil.get_forgery_word()
        if not os.path.exists(self.html_path):
            os.makedirs(self.html_path)

        if not  os.path.exists(self.word_path):
            os.makedirs(self.word_path)

        if not os.path.exists(self.forgery_path):
            os.makedirs(self.forgery_path)

    def run(self):
        while True:
            for filename in os.listdir(self.html_path):
                source_file = os.path.join(self.html_path, filename)
                dst_file = os.path.join(self.word_path, filename.replace(".html", ".docx"))
                dst_forgery_file = os.path.join(self.forgery_path, filename.replace(".html", ".docx"))
                if not os.path.exists(dst_file):
                    try:
                        logging.info(f"convert {source_file} to {dst_file}")
                        pypandoc.convert_file(source_file, 'docx', outputfile = dst_file)
                    except Exception as e:
                        logging.error(f"html2word ===============   {e.args}")
                if not os.path.exists(dst_forgery_file):
                    try:
                        logging.info(f"convert {source_file} to {dst_forgery_file}")
                        pypandoc.convert_file(source_file, 'docx', outputfile = dst_forgery_file)
                    except Exception as e:
                        logging.error(f"html2word ===============   {e.args}")

            time.sleep(20)


