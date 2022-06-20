import json
import uuid
from gensim.summarization.summarizer import summarize


def save_json(data_dic, path):
    with open(path, 'a', encoding='UTF-8') as fileout:
        json.dump(data_dic, fileout, ensure_ascii=False, indent=4)


def load_json(path):
    with open(path) as json_file:
        return json.load(json_file)

def text_rank_with_word_count(text, word_count):
    try:
        result = summarize(text["detail"], word_count=word_count)
    except:
        result = ""
    return result

def text_rank_with_ratio(text, ratio):
    try:
        result = summarize(text["detail"], ratio=ratio)
    except:
        result = ""
    return result

def text_rank():
    cities = load_json("tripadvisor_reviews.json")
    result_list = []
    for city in cities:
        print(cities.index(city))
        for review in city["reviews"]:
            review["after_text_rank_10words"] = text_rank_with_word_count(text=review, word_count=10)
            review["after_text_rank_5words"] = text_rank_with_word_count(text=review, word_count=5)
            review["after_text_rank_3words"] = text_rank_with_word_count(text=review, word_count=3)
            review["after_text_rank_02ratio"] = text_rank_with_ratio(text=review, ratio=0.2)
            review["after_text_rank_01ratio"] = text_rank_with_ratio(text=review, ratio=0.1)
            review["after_text_rank_001ratio"] = text_rank_with_ratio(text=review, ratio=0.01)
        result_list.append(city)
    save_json(result_list, "tripadvisor_reviews_textranked.json")


text_rank()