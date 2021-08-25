from collector.crawler import ArticleCrawler

class Getter():
    def __init__(self, conf):
        self.articlecrawler = ArticleCrawler(conf)
    def run(self):
        self.articlecrawler.article_crawler_1zhuan()
