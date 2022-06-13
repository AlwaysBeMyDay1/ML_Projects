from importlib.abc import Finder
from selenium.common import exceptions 
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
import json
import uuid

MOST_VISITED_CITIES = [ "Hong Kong", "Bangkok", "Macau", "Singapore", "London", "Paris", "Dubai", "Delhi", "Istanbul", "Kuala Lumpur", "New York City", "Antalya", "Mumbai", "Shenzhen", "Phuket", "Tokyo", "Rome", "Agra", "Taipei", "Pattaya", "Mecca", "Prague", "Seoul", "Guangzhou", "Osaka", "Medina", "Amsterdam", "Denpasar", "Miami", "Ho Chi Minh City", "Chennai", "Shanghai", "Los Angeles", "Jaipur", "Johor Bahru", "Barcelona", "Cairo", "Las Vegas", "Milan", "Vienna", "Athens", "Ha Long", "Berlin", "Cancun", "Moscow", "Orlando", "Madrid", "Venice", "Dublin", "Riyadh" ]
# 옵션 생성
options = webdriver.ChromeOptions()
# 창 숨기는 옵션 추가
options.add_argument("headless")

driver = webdriver.Chrome("/Users/emilynan/Desktop/Dan/chromedriver", options=options)


def save_json(data_dic, path):
    with open(path, 'a', encoding='UTF-8') as fileout:
        json.dump(data_dic, fileout, ensure_ascii=False, indent=4)


def load_json(path):
    with open(path) as json_file:
        return json.load(json_file)

# def find_reviews_url():
#     cities_file = "most_visited_cities_urls.txt"

#     result_list = []
#     with open(cities_file) as openfileobject:
#         for wikivoyage_url in openfileobject:
#             print(wikivoyage_url)
#             url_list = []
#             result_dict = {}
#             city_name = wikivoyage_url.split("-")[-1].replace(".html\n","")
#             # 옵션 생성
#             options = webdriver.ChromeOptions()
#             # 창 숨기는 옵션 추가
#             options.add_argument("headless")

#             driver = webdriver.Chrome("/Users/emilynan/Desktop/Dan/chromedriver", options=options)
#             driver.get(wikivoyage_url)
#             time.sleep(1)
#             articles = driver.find_elements(by=By.TAG_NAME, value="article")
#             for article in articles:
#                 review_url = article.find_element(by=By.TAG_NAME, value="a").get_attribute("href")
#                 url_list.append(review_url)
#             result_dict[city_name] = url_list
#             save_json(result_dict, "review_url.json")
#             result_list.append(result_dict)
#         driver.quit()
#     save_json(result_list, "review_urls.json")
def find_reviews_url():
    cities_file = "cities_Hotels_urls.txt"

    result_list = []
    with open(cities_file) as openfileobject:
        for wikivoyage_url in openfileobject:
            print(wikivoyage_url)
            url_list = []
            result_dict = {}
            city_name = wikivoyage_url.split("-")[-2].replace("_"," ")
            # 옵션 생성
            options = webdriver.ChromeOptions()
            # 창 숨기는 옵션 추가
            options.add_argument("headless")

            service = Service('/Users/emilynan/Desktop/Dan/chromedriver')
            driver = webdriver.Chrome(service=service, options=options)
            driver.get(wikivoyage_url)
            time.sleep(1)
            title_lists = driver.find_elements(by=By.CLASS_NAME, value="listing-title")
            time.sleep(0.1)
            for title_list in title_lists:
                title = title_list.find_element(by=By.CLASS_NAME, value='listing_title')
                time.sleep(0.1)
                try:
                    title.find_element(by=By.TAG_NAME, value='div')
                    time.sleep(0.1)
                    pass
                except (exceptions.NoSuchElementException, exceptions.StaleElementReferenceException):
                    review_url = title.find_element(by=By.TAG_NAME, value="a").get_attribute("href")
                    time.sleep(0.1)
                    url_list.append(review_url)
            result_dict[city_name] = url_list
            save_json(result_dict, "review_urls_Hotels(s).json")
            result_list.append(result_dict)
        driver.quit()
    save_json(result_list, "review_urls_Hotels.json")
find_reviews_url()
# popular_mentions = bLFSo bPGYE eOlCV
#  WlYyy.CETAK
# review_ul = dHjBB
def find_reviews():
    cities_list = load_json("review_urls.json")
    count = 0

    for city, poi_urls in cities_list.items():
        for poi_url in poi_urls:
            result_dict = {}.fromkeys(["poi_id","place_name","city","popular_mentions","reviews","poi_url"])
            place_name = poi_url.split("-")[-2].replace("_"," ")
            result_dict["place_name"] = place_name
            result_dict["poi_url"] = poi_url
            result_dict["city"] = city.replace("_"," ")
            result_dict["poi_id"] = str(uuid.uuid4())

            # 옵션 생성
            options = webdriver.ChromeOptions()
            # 창 숨기는 옵션 추가
            options.add_argument("headless")

            driver = webdriver.Chrome("/Users/emilynan/Desktop/Dan/chromedriver", options=options)
            driver.get(poi_url)
            time.sleep(1)
            try:
                popular_mention_section = driver.find_element(by=By.CLASS_NAME, value="bLFSo.bPGYE.eOlCV")
                popular_mention_list = popular_mention_section.find_elements(by=By.CLASS_NAME, value="WlYyy.CETAK")
                popular_mentions = []
                for popular_mention in popular_mention_list:
                    if popular_mention != "":
                        popular_mentions.append(popular_mention.text)
                result_dict["popular_mentions"] = popular_mentions
            except:
                result_dict["popular_mentions"] = []

            review_sections = driver.find_elements(by=By.CLASS_NAME, value="ffbzW._c")
            reviews = []
            try:
                for review_section in review_sections:
                    count += 1
                    if count % 100 == 0:
                        print(count)
                    review_dict = {}.fromkeys(['review_id','one_line','detail'])
                    review_list = review_section.find_elements(by=By.CLASS_NAME, value="NejBf")
                    review_dict["review_id"] = count
                    review_dict["one_line"] = review_list[0].text
                    review_dict["detail"] = review_list[1].text
                    reviews.append(review_dict)
            except:
                pass
            result_dict["reviews"] = reviews
            save_json(result_dict, "reviews_sample.json")
        driver.quit()
# find_reviews()

# driver.find_element_by_class_name('fhEMT._G.B-.z._J.Cj.R0').send_keys('Paris')
# driver.find_element_by_class_name('bmTdH.o').send_keys(Keys.ENTER)
# driver.find_element(by=By.CLASS_NAME, value="fhEMT._G.B-.z._J.Cj.R0").send_keys('Paris')
# driver.find_element(by=By.CLASS_NAME, value="bmTdH.o").click()
# time.sleep(1)