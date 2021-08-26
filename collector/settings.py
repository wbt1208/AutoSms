# from parser_conf import conf
import time
from common.common import confutil

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
if confutil.get_paramters()["source"] == "全部":
    field_map = {
        "全部":["HMCTDate", "5", ""],
        "娱乐":["acid", "1", "60665"],
        "搞笑":["acid", "1", "60666"],
        "历史":["acid", "1", "60668"]
    }
if confutil.get_paramters()["source"] in "头条号":
    field_map = {
        "全部":["HMCTDate", "5", ""],
        "娱乐":["acid", "1", "3533"],
        "搞笑":["acid", "1", "3505"],
        "历史":["acid", "1", "3540"]
    }
if confutil.get_paramters()["source"] in "百家号":
    field_map = {
        "全部":["HMCTDate", "5", ""],
        "娱乐":["acid", "1", "4"],
        "搞笑":["acid", "1", "19"],
        "历史":["acid", "1", "30"]
    }

