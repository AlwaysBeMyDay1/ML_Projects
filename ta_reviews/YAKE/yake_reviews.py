import sys
import yake
sys.path.append("../")
from def_pintween.save_or_load_json import save_json, load_json

def extract_keywords():
    restaurants = load_json("reviews_Restaurants.json")

    kw_extractor = yake.KeywordExtractor(top=5, stopwords=None)
    result_list = []
    for restaurant in restaurants:
        for review in restaurant['reviews']:
            result_dict = {}
            one_line_dict = {}
            detail_dict = {}
            keywords = kw_extractor.extract_keywords(review['one_line'])
            for kw, score in keywords:
                one_line_dict[kw] = score
            keywords = kw_extractor.extract_keywords(review['detail'])
            for kw, score in keywords:
                detail_dict[kw] = score
            result_dict["review_id"] = review["review_id"]
            result_dict["plae_name"] = restaurant["place_name"]
            result_dict["category"] = restaurant["category"]
            result_dict["one_line_yake"] = one_line_dict
            result_dict["detail_yake"] = detail_dict
            result_list.append(result_dict)
            save_json(result_dict, "yake_Restaurants.json")


extract_keywords()