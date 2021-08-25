from collector.crawler import ArticleCrawler
from parser_conf import conf

class Getter():
    def __init__(self):
        self.articlecrawler = ArticleCrawler(conf)
    def run(self):
        self.articlecrawler.article_crawler_1zhuan()
