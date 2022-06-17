import re, os, sys
import yake

sys.path.append("../")
from def_pintween.save_or_load_json import save_json, load_json
from def_pintween.find_reduplication import get_reduplicated_num
from def_pintween.word_tag import extract_proper_noun ,remove_proper_noun, distinct_proper_noun, remove_adjective, extract_noun

# tripadvisor review 추출 -> proper noun 제거 -> make all lower
# oneline, detail 각자끼리 사용 빈도 추정 
 
THIS_DIR = os.path.dirname(os.path.abspath(__file__))

language = "en"
max_ngram_size = 5
deduplication_threshold = 0.9
num_of_kw = 5
custom_kw_extractor = yake.KeywordExtractor(lan=language, n=max_ngram_size, dedupLim=deduplication_threshold, top=num_of_kw,features=None)

def similar_tfidf_oneline(category):
    os.chdir(os.path.join(THIS_DIR, 'results_ngram5'))
    # review_list = load_json(f"yake_ngram5_{category}_cleaned_pn.json")
    # review_list = load_json(f"yake_ngram5_{category}_adj.json")
    review_list = load_json(f"yake_ngram5_{category}_noun.json")
    one_line_list = []
    for review in review_list:
        one_lines = [re.sub('[^A-Za-z0-9\s]', '', one_line.lower()) for one_line in list(review['one_line_yake'].keys())] #dict
        one_line_list += one_lines
    # save_json(sorted(get_reduplicated_num(one_line_list).items(),key = lambda item: item[1], reverse=True), f"kw_oneline_{category}.json")
    # save_json(sorted(get_reduplicated_num(one_line_list).items(),key = lambda item: item[1], reverse=True), f"kw_oneline_{category}_adj.json")
    save_json(sorted(get_reduplicated_num(one_line_list).items(),key = lambda item: item[1], reverse=True), f"kw_oneline_{category}_noun.json")


def similar_tfidf_detail(category):
    os.chdir(os.path.join(THIS_DIR, 'results_ngram5'))
    # review_list = load_json(f"yake_ngram5_{category}_cleaned_pn.json")
    # review_list = load_json(f"yake_ngram5_{category}_adj.json")
    review_list = load_json(f"yake_ngram5_{category}_noun.json")

    detail_review_list = []
    for review in review_list:
        detail_reviews = [re.sub('[^A-Za-z0-9\s]', '', one_line.lower()) for one_line in list(review['detail_yake'].keys())] #dict
        detail_review_list += detail_reviews
    # save_json(sorted(get_reduplicated_num(detail_review_list).items(),key = lambda item: item[1], reverse=True), f"kw_detail_{category}.json")
    # save_json(sorted(get_reduplicated_num(detail_review_list).items(),key = lambda item: item[1], reverse=True), f"kw_detail_{category}_adj.json")
    save_json(sorted(get_reduplicated_num(detail_review_list).items(),key = lambda item: item[1], reverse=True), f"kw_detail_{category}_noun.json")

# 한 단어 다 빼고 sorted 돌리기

def extract_keywords(category):
    os.chdir(os.path.join(THIS_DIR, 'resources'))
    restaurants = load_json(f"reviews_{category}.json")

    result_list = []
    for restaurant in restaurants:
        for review in restaurant['reviews']:
            one_line_dict = {}
            detail_dict = {}
            keywords = custom_kw_extractor.extract_keywords(extract_noun(review['one_line']))
            for kw, score in keywords:
                one_line_dict[kw] = score
            keywords = custom_kw_extractor.extract_keywords(extract_noun(review['detail']))
            for kw, score in keywords:
                detail_dict[kw] = score

            result_dict_keys = ['review_id','place_name', 'category', 'one_line_yake', 'detail_yake']
            result_dict_values = [review["review_id"], restaurant["place_name"], restaurant["category"], one_line_dict, detail_dict]
            result_dict = dict(zip(result_dict_keys, result_dict_values))
            result_list.append(result_dict)

    os.chdir(os.path.join(THIS_DIR, 'results_ngram5'))
    # save_json(result_list, f"yake_ngram5_{category}_cleaned_pn.json")
    # save_json(result_list, f"yake_ngram5_{category}_adj.json")
    save_json(result_list, f"yake_ngram5_{category}_noun.json")


def bi_gram(category):
    os.chdir(os.path.join(THIS_DIR, 'results_ngram5'))
    detail_kw_list = load_json(f"kw_detail_{category}.json")
    oneline_kw_list = load_json(f"kw_oneline_{category}.json")

    detail_kw_result_list = []
    for kw in detail_kw_list:
        if len(kw[0].split()) > 1:
            detail_kw_result_list.append(kw)

    oneline_kw_result_list = []
    for kw in oneline_kw_list:
        if len(kw[0].split()) > 1:
            oneline_kw_result_list.append(kw)

    save_json(detail_kw_result_list, f'kw_detail_{category}_bigram.json')
    save_json(oneline_kw_result_list, f'kw_oneline_{category}_bigram.json')

bi_gram("Restaurants")
# extract_keywords("Attractions")
# similar_tfidf_oneline("Attractions")
# similar_tfidf_detail("Attractions")

