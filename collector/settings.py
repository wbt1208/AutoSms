# from parser_conf import conf
import time
date = time.strftime('%Y-%m-%d 00:00',time.localtime(time.time()- 6 * 24 * 60 * 60))
paramters_map = {
    "source": "CID",
    "field": ["Where[0][Name]", "Where[0][Symbol]", "Where[0][Value]"],
    "keyword":["Where[2][Name]","Where[2][Symbol]", "Where[2][Value]"]
}
source_map = {
    "全部": "0",
    "百家号": "2",
    "头条号": "5"
}

field_map = {
    "全部":["HMCTDate", "5", f"{date}"],
    "娱乐":["acid", "1", "60665"],
    "搞笑":["acid", "1", "60666"]
}

keyword_map = {
    "":["hmcttype", "1", "1"],
    "not mull": ["hmcttype", "2", "kw"]
}


