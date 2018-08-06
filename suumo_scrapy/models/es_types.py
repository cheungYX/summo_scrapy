__author__ = 'bobby'

from datetime import datetime
from elasticsearch_dsl import (
    connections,
    DocType,
    Document,
    analyzer,
    Completion,
    Keyword,
    Index,
    Date,
    Nested,
    Boolean,
    Float,
    Integer,
    Ip,
    Text
)
from elasticsearch_dsl.analysis import CustomAnalyzer as _CustomAnalyzer

from elasticsearch_dsl.connections import connections
connections.create_connection(hosts=["localhost"])

class CustomAnalyzer(_CustomAnalyzer):
    def get_analysis_definition(self):
        return {}


# ik_analyzer = CustomAnalyzer("ik_max_word", filter=["lowercase"])

class Article(Document):

    name = Text(analyzer="kuromoji_analyzer")
    price = Integer()
    url = Keyword()
    url_object_id = Keyword()

    address = Text(analyzer="kuromoji_analyzer")
    stations = Keyword()
    size = Keyword()
    area = Float()
    
    build_year = Integer()
    floor = Keyword()
    crawl_time = Date()

    class Index:
        name = 'suumo'
        settings = {
          "number_of_shards": 1,
        }

if __name__ == "__main__":
    Article.init()