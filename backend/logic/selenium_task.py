import requests
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
#from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException

#from webdriver_manager.chrome import ChromeDriverManager
from .datapreprocessing import preprocessing
from .models import Car

def retrieve_car_links(url):
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")
        car_links = soup.select('a.m-link-ticket')
        return [link["href"] for link in car_links]
    else:
        return []

def retrieve_car_page(url):
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    #need to get url from selenium-google container
    driver = webdriver.Remote(
        command_executor='http://192.168.0.4:4444',
        options=options
        )
    try:
        driver.get(url)
        title = driver.find_element(By.CSS_SELECTOR, '#heading-cars > div > h1').text
        price_usd = driver.find_element(
            By.CSS_SELECTOR, 
            '#showLeftBarView > section.price.mb-15.mhide > div.price_value > strong'
            ).text
        odometer = driver.find_element(
            By.CSS_SELECTOR, 
        '#showLeftBarView > section.price.mb-15.mhide > div.base-information.bold > span').text
        try:
            username = driver.find_element(
                By.CSS_SELECTOR, 
                '#userInfoBlock > div.seller_info.mb-15 > div > div.seller_info_name.bold').text
        except NoSuchElementException:
            try:
                username = driver.find_element(
                    By.CSS_SELECTOR,
                    '#userInfoBlock > div.seller_info.mb-15 > div > h4 > a'
                    ).text
            except NoSuchElementException:
                username = "N/A"
        try:    
            image_element = driver.find_element(By.CSS_SELECTOR, 
                                                '#photosBlock > div.gallery-order.carousel > div.carousel-inner._flex > div.photo-620x465.loaded > picture > img')
            image_url = image_element.get_attribute("src")
        except NoSuchElementException:
            image_url = "N/A"
        image_count = driver.find_element(By.CSS_SELECTOR, 
                    '#photosBlock > div.preview-gallery.mhide > div.action_disp_all_block > a').text
        
        try:
            car_number = driver.find_element(By.CLASS_NAME, 'state-num.ua').text
        except NoSuchElementException:
            car_number = "N/A"
            
        try:
            car_vin = driver.find_element(By.CLASS_NAME, "label-vin").text
        except NoSuchElementException:
            car_vin = "N/A"
        wait = WebDriverWait(driver, 20)
        phone_click = wait.until(
            EC.element_to_be_clickable(
                (By.CSS_SELECTOR, '#phonesBlock > div:nth-child(1) > span > a')
        ))
        driver.execute_script("arguments[0].click();", phone_click)
        phone_number_element = wait.until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, '#show-phone > div.modal-body > div.list-phone > div.popup-successful-call-desk.size24.bold.green.mhide.green')))
        phone_number = phone_number_element.text
        df = pd.DataFrame({
            "url": url,
            "title": title,
            "price_usd": price_usd,
            "odometer": odometer,
            "username": username,
            "phone_number": phone_number,
            "image_url": image_url,
            "images_count": image_count,
            "car_number": car_number,
            "car_vin": car_vin
        }, index=[0])
        return df
    except Exception as e:
        raise e
    finally:
        driver.quit()
        
def constructor():
    retrieve_cars = retrieve_car_links("https://auto.ria.com/uk/car/used/")
    merged_df = pd.DataFrame(columns=["url", "title", "price_usd", "odometer", "username", "phone_number", "image_url", "images_count", "car_number", "car_vin"])
    for cars_link in retrieve_cars:    
        car_df = retrieve_car_page(cars_link)
        merged_df = pd.concat([merged_df, car_df], ignore_index=True)
    merged_df.to_csv("car_data.csv", index=False)
    preprocessing()
    
def add_to_database():
    df = pd.read_csv("car_data.csv")
    for index, row in df.iterrows():
        Car.objects.create(
            url=row['url'],
            title=row['title'],
            price_usd=row['price_usd'],
            odometer=row['odometer'],
            username=row['username'],
            phone_number=row['phone_number'],
            image_url=row['image_url'],
            images_count=row['images_count'],
            car_number=row['car_number'],
            car_vin=row['car_vin'],
            )

    
