# HP Product recommender system
from selenium import webdriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.common.exceptions import StaleElementReferenceException,NoSuchElementException
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
import time

products = pd.DataFrame(columns=['Model','Memory','Storage','Operating System','Graphics','Size','Weight','Purpose','Price'])

driver = webdriver.Chrome(executable_path = r"C:\Program Files\Selenium\chromedriver.exe")
driver.get(r"https://store.hp.com/in-en/default/hp-laptop-family#home")
driver.maximize_window()
time.sleep(3)
actions = ActionChains(driver)
driver.execute_script("window.scrollTo(0,200)")

def get_item_details():
    driver.execute_script("window.scrollTo(0,100)")
    time.sleep(3)
    driver.find_element_by_partial_link_text("Specifications").click()
    model = driver.title.split("|")[0]
    os = driver.find_element_by_xpath("//tr[contains(@class,'item')]//td[contains(@data-th,'Operating system')]").text
    processor = driver.find_element_by_xpath("//tr[contains(@class,'item')]//td[contains(@data-th,'Processor Name')]").text.split("(")[0].strip()

    memory_element = driver.find_element_by_xpath("//tr[contains(@class,'item')]//td[contains(@data-th,'Memory')]")
    actions.move_to_element(memory_element)
    memory = memory_element.text.strip()
    
    storage = driver.find_element_by_xpath("//tr[contains(@class,'item')]//td[contains(@data-th,'Hard drive description')]").text.split("PCIe®")[0].strip()+driver.find_element_by_xpath("//tr[contains(@class,'item')]//td[contains(@data-th,'Storage type')]").text
    
    try:
        size = driver.find_element_by_xpath("//tr[contains(@class,'item')]//td[contains(@data-th,'Display HP')]").text.split("(")[1].split(")")[0].strip()
    except NoSuchElementException:
        size = driver.find_element_by_xpath("//tr[contains(@class,'item')]//td[contains(@data-th,'Display')]").text.split("(")[1].split(")")[0].strip()
    try:
        weight = driver.find_element_by_xpath("//tr[contains(@class,'item')]//td[contains(@data-th,'Package weight')]").text
    except NoSuchElementException:
        weight = driver.find_element_by_xpath("//tr[contains(@class,'item')]//td[contains(@data-th,'Weight')]").text
    
    driver.execute_script("window.scrollTo(0,40)")
    price = driver.find_element_by_xpath("//span[contains(@data-price-type,'finalPrice')]/span[contains(@class,'price')]").text    
    
    # products = products.append({'Model':model,"Memory":memory,"Storage":storage,'Operating System':os,'Processor':processor,'Size':size,'Weight':weight,'Price':price},ignore_index=True)
    print(f"Model: {model}\nOS: {os}\nProcessor: {processor}\nRAM: {memory}\nStorage: {storage}\nSize: {size}\nWeight: {weight}\nCost: {price}\n")    
    driver.back()    

def get_products(product_id):
    driver.find_element_by_id("product"+str(product_id)).click()
    product_links = driver.find_elements_by_xpath("//div[contains(@class,'product details product-item-details')]//strong[contains(@class,'product name product-item-name')]/a[contains(@class,'product-item-link')]")
    print(product_links)
    for id in range(len(product_links)):
        print(f"Iteration: {id+1}")
        link = driver.find_element_by_xpath("//*[@id='category.product.list']/div[2]/ol/li["+str(id+1)+"]//a[contains(@class,'product photo product-item-photo')]")
        try:
            actions.move_to_element(link)
            link.click()
            get_item_details()
            driver.implicitly_wait(5)
        except StaleElementReferenceException:
            print("Stale Element Exception occurred during object identification.")
            
get_products(3)
driver.close()
    
