from collector.crawler import ArticleCrawler

class Getter():
    def __init__(self):
        self.articlecrawler = ArticleCrawler()
    def run(self):
        self.articlecrawler.article_crawler_1zhuan()
