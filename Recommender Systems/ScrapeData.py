# HP Product recommender system
from selenium import webdriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.common.exceptions import StaleElementReferenceException,NoSuchElementException
from bs4 import BeautifulSoup
import logging
import pandas as pd
import numpy as np
import time

products = pd.DataFrame(columns=['Model','Product','Memory','Storage','Operating System','Graphics','Size','Weight','Purpose','Price'])

driver = webdriver.Chrome(executable_path = r"C:\Program Files\Selenium\chromedriver.exe")
driver.get(r"https://store.hp.com/in-en/default/hp-laptop-family#home")
driver.maximize_window()
time.sleep(3)
actions = ActionChains(driver)
driver.execute_script("window.scrollTo(0,200)")

def get_item_details(model):
    driver.execute_script("window.scrollTo(0,100)")
    time.sleep(3)
    driver.find_element_by_partial_link_text("Specifications").click()
    product = driver.title.split("|")[0]
    
    try:
        os = driver.find_element_by_xpath("//tr[contains(@class,'item')]//td[contains(@data-th,'Operating system')]").text
    except NoSuchElementException:
        os = None
    try:    
        graphics = driver.find_element_by_xpath("//tr[contains(@class,'item')]//td[contains(@data-th,'Graphics')]").text
    except NoSuchElementException:
        graphics = None
    try:    
        processor = driver.find_element_by_xpath("//tr[contains(@class,'item')]//td[contains(@data-th,'Processor Name')]").text.split("(")[0].strip()
    except NoSuchElementException:
        processor = None
    try:
        memory_element = driver.find_element_by_xpath("//tr[contains(@class,'item')]//td[contains(@data-th,'Memory')]")
        actions.move_to_element(memory_element)
        memory = memory_element.text.strip()
    except NoSuchElementException:
        memory = None
    try:
        storage = driver.find_element_by_xpath("//tr[contains(@class,'item')]//td[contains(@data-th,'Hard drive description')]").text.split("PCIe®")[0].strip()+driver.find_element_by_xpath("//tr[contains(@class,'item')]//td[contains(@data-th,'Storage type')]").text
    except NoSuchElementException:
        storage = None
    try:
        size = driver.find_element_by_xpath("//tr[contains(@class,'item')]//td[contains(@data-th,'Display')]").text.split("(")[1].split(")")[0].strip()
    except NoSuchElementException:
        try:
            size = driver.find_element_by_xpath("//tr[contains(@class,'item')]//td[contains(@data-th,'Display HP')]").text.split("(")[1].split(")")[0].strip()
        except NoSuchElementException:
            size = None
    try:
        weight = driver.find_element_by_xpath("//tr[contains(@class,'item')]//td[contains(@data-th,'Weight')]").text
    except NoSuchElementException:
        weight = None
    try:
        price = driver.find_element_by_xpath("//span[contains(@data-price-type,'finalPrice')]/span[contains(@class,'price')]").text    
    except NoSuchElementException:
        price = None
    
    features = {'Model':model,'Product':product,"Memory":memory,"Storage":storage,'Operating System':os,'Graphics':graphics,'Processor':processor,'Size':size,'Weight':weight,'Price':price}
    global products
    products = products.append(features,ignore_index=True)
    # print(f"Product: {product}\nOS: {os}\nProcessor: {processor}\nRAM: {memory}\nStorage: {storage}\nSize: {size}\nWeight: {weight}\nCost: {price}\n")    
    driver.back()    

def get_products(product_id,model_links,path_prefix,path_suffix,model):
    driver.implicitly_wait(5)
    driver.find_element_by_id("product"+str(product_id)).click()
    product_links = driver.find_elements_by_xpath(model_links)
    print(product_links)
    for id in range(len(product_links)):
        print(f"Iteration: {id+1}")
        link = driver.find_element_by_xpath(path_prefix+str(id+1)+path_suffix)
        try:
            actions.move_to_element(link)
            link.click()
            get_item_details(model)
            driver.implicitly_wait(5)
        except StaleElementReferenceException:
            print("Stale Element Exception occurred during object identification.")
    driver.back()
    driver.implicitly_wait(5)

try:
    products_link = "//div[contains(@class,'product details product-item-details')]//strong[contains(@class,'product name product-item-name')]/a[contains(@class,'product-item-link')]"
    products_path_prefix = "//*[@id='category.product.list']/div[2]/ol/li["
    products_path_suffix = "]//a"
    get_products(1,products_link,products_path_prefix,products_path_suffix,'Pavilion')
    get_products(2,products_link,products_path_prefix,products_path_suffix,'Envy')
    get_products(3,products_link,products_path_prefix,products_path_suffix,'Spectre')
    get_products(4,products_link,products_path_prefix,products_path_suffix,'Essential')
    products['Purpose'] = 'Home'
    driver.find_element_by_xpath("//*[@id='brands']/div/div/div/div/div[1]/div/div/div/ul/li[3]/a").click()
    driver.execute_script("window.scrollTo(0,100)")
    driver.implicitly_wait(5)
    get_products(5,products_link,products_path_prefix,products_path_suffix,'Omen')
    get_products(6,products_link,products_path_prefix,products_path_suffix,'Pavilion Gaming')
    products['Purpose'].fillna('Gaming',inplace = True)
    driver.find_element_by_xpath("//*[@id='brands']/div/div/div/div/div[1]/div/div/div/ul/li[4]/a").click()
    driver.execute_script("window.scrollTo(0,100)")
    driver.implicitly_wait(5)
    get_products(7,products_link,products_path_prefix,products_path_suffix,'EliteBook')
    get_products(8,products_link,products_path_prefix,products_path_suffix,'ProBook')    
    get_products(9,products_link,products_path_prefix,products_path_suffix,'ZBook')
    get_products(11,products_link,products_path_prefix,products_path_suffix,'Essential Business')
    products['Purpose'].fillna('Business',inplace = True)
    driver.close()
    
except Exception as e:
    logging.error(f'Error occurred while collecting data: {str(e)}')
    driver.close()

products.head()
np.shape(products)
print(f"Products per model:\n{products['Model'].value_counts()}")
