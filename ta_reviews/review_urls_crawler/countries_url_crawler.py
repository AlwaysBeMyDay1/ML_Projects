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

def save_json(data_dic, path):
    with open(path, 'a', encoding='UTF-8') as fileout:
        json.dump(data_dic, fileout, ensure_ascii=False, indent=4)


def load_json(path):
    with open(path) as json_file:
        return json.load(json_file)


def open_file(file_name):
    with open(file_name) as openfileobject:
        url_list = list(openfileobject)
        return url_list

service = Service('/Users/emilynan/Desktop/Dan/chromedriver')
# 옵션 생성
options = webdriver.ChromeOptions()
# 창 숨기는 옵션 추가
options.add_argument("headless")
driver = webdriver.Chrome(service=service, options=options)


def find_reviews_url_attractions():
    openfileobject = open_file("most_visited_cities_urls.txt")
    result_list = []
    for wikivoyage_url in openfileobject:
        print(wikivoyage_url)
        url_list = []
        result_dict = {}
        city_name = wikivoyage_url.split("-")[-1].replace(".html\n","")
        
        driver.get(wikivoyage_url)
        time.sleep(1)
        articles = driver.find_elements(by=By.TAG_NAME, value="article")
        for article in articles:
            review_url = article.find_element(by=By.TAG_NAME, value="a").get_attribute("href")
            url_list.append(review_url)
        result_dict[city_name] = url_list
        save_json(result_dict, "review_url.json")
        result_list.append(result_dict)
    driver.quit()
    save_json(result_list, "review_urls.json")


def find_reviews_url_hotels():
    openfileobject = open_file("cities_Hotels_urls.txt")
    result_list = []
    for wikivoyage_url in openfileobject:
        print(wikivoyage_url)
        url_list = []
        result_dict = {}
        city_name = wikivoyage_url.split("-")[-2].replace("_"," ")
        
        driver.get(wikivoyage_url)
        time.sleep(1)
        title_lists = driver.find_elements(by=By.CLASS_NAME, value="listing-title")
        for title_list in title_lists:
            try:
                title = title_list.find_element(by=By.CLASS_NAME, value='listing_title')
                try:
                    title.find_element(by=By.TAG_NAME, value='div')
                    pass
                except (exceptions.NoSuchElementException, exceptions.StaleElementReferenceException):
                    try:
                        review_url = title.find_element(by=By.TAG_NAME, value="a").get_attribute("href")
                        url_list.append(review_url)
                    except (exceptions.NoSuchElementException, exceptions.StaleElementReferenceException):
                        pass
            except (exceptions.NoSuchElementException, exceptions.StaleElementReferenceException):
                pass
        result_dict[city_name] = url_list
        save_json(result_dict, "review_urls_Hotels(s).json")
        result_list.append(result_dict)
        driver.quit()
    save_json(result_list, "review_urls_Hotels.json")


def find_reviews_url_restaurants():
    openfileobject = open_file("cities_Restaurants_urls.txt")
    result_list = []
    for wikivoyage_url in openfileobject:
        print(wikivoyage_url)
        url_list = []
        result_dict = {}
        city_name = wikivoyage_url.split("-")[-1].replace(".html\n","")
        
        driver.get(wikivoyage_url)
        time.sleep(1)
        articles = driver.find_elements(by=By.CLASS_NAME, value="OhCyu")
        for article in articles:
            review_url = article.find_element(by=By.TAG_NAME, value="a").get_attribute("href")
            url_list.append(review_url)
        result_dict[city_name] = url_list
        save_json(result_dict, "review_urls_Restaurants(s).json")
        result_list.append(result_dict)
    driver.quit()
    save_json(result_list, "review_urls_Restaurants.json")


find_reviews_url_restaurants()
