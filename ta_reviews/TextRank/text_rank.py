import json
import uuid
from gensim.summarization.summarizer import summarize


def save_json(data_dic, path):
    with open(path, 'a', encoding='UTF-8') as fileout:
        json.dump(data_dic, fileout, ensure_ascii=False, indent=4)


def load_json(path):
    with open(path) as json_file:
        return json.load(json_file)

def text_rank():
    cities = load_json("tripadvisor_reviews.json")
    result_list = []
    for city in cities:
        print(cities.index(city))
        for review in city["reviews"]:
            try:
                review["after_text_rank_10words"] = summarize(review["detail"], word_count=10)
            except:
                review["after_text_rank_10words"] = ""
            try:
                review["after_text_rank_5words"] = summarize(review["detail"], word_count=5)
            except:
                review["after_text_rank_5words"] = ""
            try:
                review["after_text_rank_1words"] = summarize(review["detail"], word_count=1)
            except:
                review["after_text_rank_1words"] = ""
            try:
                review["after_text_rank_02ratio"] = summarize(review["detail"], ratio=0.2)
            except:
                review["after_text_rank_02ratio"] = ""
            try:
                review["after_text_rank_01ratio"] = summarize(review["detail"], ratio=0.1)
            except:
                review["after_text_rank_01ratio"] = ""
            try:
                review["after_text_rank_001ratio"] = summarize(review["detail"], ratio=0.01)
            except:
                review["after_text_rank_001ratio"] = ""
        result_list.append(city)
    
    save_json(result_list, "tripadvisor_reviews_textranked.json")



text_rank()