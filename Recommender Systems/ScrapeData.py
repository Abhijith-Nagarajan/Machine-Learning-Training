# HP Product recommender system
from selenium import webdriver
from bs4 import BeautifulSoup
from dataclasses import dataclass
import time

driver = webdriver.Chrome(executable_path = r"C:\Program Files\Selenium\chromedriver.exe")
driver.get(r"https://store.hp.com/in-en/default/hp-laptop-family#home")
driver.maximize_window()
time.sleep(3)
driver.execute_script("window.scrollTo(0,200)")

# =============================================================================
# @dataclass
# class Product:
#     name: str
#     processor: str
#     os: str
#     ram: str
#     storage: str
#     graphics: str
#     size: str
#     purpose: str
#     price: int
#     
# =============================================================================

def return_product(soup,tag,field):
    items = []
    for item in list(soup.find_all(tag,class_ = field)):
        items.append(item.get_text().strip())
    return items
        
def fetch_item_details(soup):
    driver.execute_script("window.scrollTo(0,200)")
    models = return_product(soup,'a','product-item-link')
    del models[-1]
    print(f"Models:\n{models}\n")
    processors = return_product(soup,'li','processorfamily')
    print(f"Processors:\n{processors}\n")
    os = return_product(soup,'li','osinstalled')
    print(f"Operating Systems:\n{os}\n")
    display = return_product(soup,'li','display-displaydes')
    print(f"Display:\n{display}\n")
    graphics = return_product(soup,'li','graphicseg_01card_01-graphicseg_02card_01')
    print(f"Graphics:\n{graphics}\n")
    memory = return_product(soup,'li','memstdes_01')
    print(f"Memory:\n{memory}\n")
    weight = return_product(soup,'li','weightmet')
    print(f"Weight:\n{weight}\n")
    price = return_product(soup,'span','price')
    print(f"Cost:\n{price}\n")
    
def get_products_info(product_id):
    driver.find_element_by_id("product"+str(product_id)).click()
    page_source = driver.page_source
    soup = BeautifulSoup(page_source,'html')
    fetch_item_details(soup)
    driver.back()

get_products_info(3)
time.sleep(5)
driver.close()
    
