from importlib.abc import Finder
from langcodes import TERRITORY_REPLACEMENTS
from pandas import value_counts
from selenium.common import exceptions 
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
import json
import uuid


MOST_VISITED_CITIES = [ "Hong Kong", "Bangkok", "Macau", "Singapore", "London", "Paris", "Dubai", "Delhi", "Istanbul", "Kuala Lumpur", "New York City", "Antalya", "Mumbai", "Shenzhen", "Phuket", "Tokyo", "Rome", "Agra", "Taipei", "Pattaya", "Mecca", "Prague", "Seoul", "Guangzhou", "Osaka", "Medina", "Amsterdam", "Denpasar", "Miami", "Ho Chi Minh City", "Chennai", "Shanghai", "Los Angeles", "Jaipur", "Johor Bahru", "Barcelona", "Cairo", "Las Vegas", "Milan", "Vienna", "Athens", "Ha Long", "Berlin", "Cancun", "Moscow", "Orlando", "Madrid", "Venice", "Dublin", "Riyadh" ]

def save_json(data_dic, path):
    with open(path, 'a', encoding='UTF-8') as fileout:
        json.dump(data_dic, fileout, ensure_ascii=False, indent=4)


def load_json(path):
    with open(path) as json_file:
        return json.load(json_file)

service = Service('/Users/emilynan/Desktop/Dan/chromedriver')
# 옵션 생성
options = webdriver.ChromeOptions()
# 창 숨기는 옵션 추가
options.add_argument("headless")
options.add_argument('--disable-blink-features=AutomationControlled')
driver = webdriver.Chrome(service=service, options=options)

# popular_mentions = bLFSo bPGYE eOlCV
# WlYyy.CETAK
# review_ul = dHjBB
def find_reviews_attractions():
    cities_list = load_json("review_urls_Attractions.json")
    count = 40233

    for city, poi_urls in cities_list.items():
        for poi_url in poi_urls:
            result_dict = {}.fromkeys(["poi_id", "poi_url", "place_name", "city", "address", "category", "description", "popular_mentions", "reviews"])
            place_name = poi_url.split("-")[-2].replace("_"," ")
            result_dict["place_name"] = place_name
            result_dict["poi_url"] = poi_url
            result_dict["city"] = city.replace("_"," ")
            result_dict["poi_id"] = str(uuid.uuid4())

            driver.get(poi_url)
            time.sleep(2)

            # address
            try:
                address_section = driver.find_element(by=By.CLASS_NAME, value="dIDBU.MJ")
                address = address_section.find_element(by=By.CLASS_NAME, value="WlYyy.cacGK.Wb").text
            except:
                address = ""
            result_dict["address"] = address

            # category
            try:
                category_section = driver.find_element(by=By.CLASS_NAME, value='hxQKk')
                category = category_section.find_element(by=By.CLASS_NAME, value="pIRBV._T.KRIav").text
            except:
                category = ""
            result_dict["category"] = category

            # description
            try :
                description_section = driver.find_element(by=By.CLASS_NAME, value='dYtkw')
                description = description_section.find_element(by=By.CLASS_NAME, value="duhwe._T.bOlcm").text
            except:
                description = ""
            result_dict["description"] = description

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
            for review_section in review_sections:
                try:
                    review_dict = {}.fromkeys(['review_id','one_line','detail'])
                    review_list = review_section.find_elements(by=By.CLASS_NAME, value="NejBf")
                    review_dict["review_id"] = count
                    review_dict["one_line"] = review_list[0].text
                    review_dict["detail"] = review_list[1].text
                    reviews.append(review_dict)
                    count += 1
                    if count % 100 == 0 : print(count)
                except:
                    pass
            result_dict["reviews"] = reviews
            save_json(result_dict, "reviews_Attractions.json")
    driver.quit()


def find_reviews_restaurants():
    cities_list = load_json("review_urls_Restaurants.json")
    count = 408

    for city, poi_urls in cities_list.items():
        for poi_url in poi_urls:
            result_dict = {}.fromkeys(["poi_id", "poi_url", "place_name", "city", "address", "category", "description", "reviews"])
            place_name = poi_url.split("-")[-2].replace("_"," ")
            result_dict["poi_id"] = str(uuid.uuid4())
            result_dict["poi_url"] = poi_url
            result_dict["place_name"] = place_name
            result_dict["city"] = city.replace("_"," ")

            driver.get(poi_url)
            time.sleep(3)
            
            # address
            result_dict["address"] = driver.find_element(by=By.CLASS_NAME, value='brMTW').text
            
            # category
            categories = driver.find_elements(by=By.CLASS_NAME, value='drUyy')
            result_dict["category"] = [category.text for category in categories]

            # description
            try:
                description = driver.find_element(by=By.CLASS_NAME, value='epsEZ').text
            except:
                description = ""
            result_dict["description"] = description

            # reviews
            review_sections = driver.find_elements(by=By.CLASS_NAME, value="review-container")
            reviews = []
            for review_section in review_sections:
                try:
                    review_dict = {}.fromkeys(['review_id','one_line','detail'])
                    review_dict["review_id"] = count
                    review_dict["one_line"] = review_section.find_element(by=By.CLASS_NAME, value="noQuotes").text
                    review_dict["detail"] = review_section.find_element(by=By.CLASS_NAME, value="partial_entry").text
                    reviews.append(review_dict)
                    count += 1
                    if count % 100 == 0 : print(count)
                except:
                    pass
            result_dict["reviews"] = reviews

            save_json(result_dict, "reviews_Restaurants.json")
    driver.quit()

def remove_reduplication():
    dict = load_json("review_urls_Hotels(s).json")
    result_dict = {}
    for city, url_list in dict.items():
        result_dict[city] = list(set(url_list))
    save_json(result_dict, "review_urls_Hotels.json")

def find_reviews_hotels():
    cities_list = load_json("review_urls_Hotels.json")
    count = 21708

    for city, poi_urls in cities_list.items():
        for poi_url in poi_urls:
            result_dict = {}.fromkeys(["poi_id", "poi_url", "place_name", "city", "address", "category", "description", "reviews"])
            place_name = poi_url.split("-")[-2].replace("_"," ")
            result_dict["poi_id"] = str(uuid.uuid4())
            result_dict["poi_url"] = poi_url
            result_dict["place_name"] = place_name
            result_dict["city"] = city.replace("_"," ")
            result_dict["category"] = "Hotels"

            driver.get(poi_url)
            time.sleep(3)
            
            # address
            try:
                address = driver.find_element(by=By.CLASS_NAME, value='ceIOZ.yYjkv').text
            except:
                address = ""
            result_dict["address"] = address

            # description
            try:
                description = driver.find_element(by=By.CLASS_NAME, value='pIRBV._T').text
            except:
                description = ""
            result_dict["description"] = description

            # reviews
            review_sections = driver.find_elements(by=By.CLASS_NAME, value="cqoFv._T")
            reviews = []
            for review_section in review_sections:
                try:
                    review_dict = {}.fromkeys(['review_id','one_line','detail'])
                    review_dict["review_id"] = count
                    review_dict["one_line"] = review_section.find_element(by=By.CLASS_NAME, value="fCitC").text
                    review_dict["detail"] = review_section.find_element(by=By.CLASS_NAME, value="duhwe._T.bOlcm.dMbup").text
                    reviews.append(review_dict)
                    count += 1
                    if count % 100 == 0 : print(count)
                except:
                    pass
            result_dict["reviews"] = reviews

            save_json(result_dict, "reviews_Hotels.json")
    driver.quit()

# find_reviews()
# find_reviews_hotels()
find_reviews_attractions()

# driver.find_element_by_class_name('fhEMT._G.B-.z._J.Cj.R0').send_keys('Paris')
# driver.find_element_by_class_name('bmTdH.o').send_keys(Keys.ENTER)
# driver.find_element(by=By.CLASS_NAME, value="fhEMT._G.B-.z._J.Cj.R0").send_keys('Paris')
# driver.find_element(by=By.CLASS_NAME, value="bmTdH.o").click()
# time.sleep(1)