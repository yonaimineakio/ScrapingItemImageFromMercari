import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.common.exceptions import StaleElementReferenceException
from tqdm import tqdm
from typing import Any
from Config import (
    INPUT_PATH,
    DRIVER_PATH
)
import re
import os

driver :Any

## init process
def initData() -> Any:
    global driver
    cService= webdriver.ChromeService(executable_path=DRIVER_PATH)
    options = Options()
    options.add_argument('--headless')
    driver = webdriver.Chrome(service=cService, options=options)



#load process
def load(path: str) -> list[str]:
    urls =[]
    with open(path) as f:
        for line in f:
            urls.append(line)
    return urls


#retrive process
def retrive(driver: Any, urls: list[str]) -> None:
    for url in urls:
        item_id = url.split("/")[4].split()
        driver.get(url)
        time.sleep(1)

        #get title
        card_title = re.sub(re.compile('<.*?>|　|/'), '', driver.find_element(By.XPATH, value="//h1").get_attribute("outerHTML"))
        if not os.path.isdir(card_title):
            os.mkdir(f"./{card_title}")

        #get picture elements
        picture_div = driver.find_elements(By.XPATH, value="//figure/div/picture/img")
        time.sleep(1)
        image_links = set([ ele.get_attribute("src") if ele.get_attribute("alt") == "のサムネイル" else "skip" for ele in picture_div ])
        if len(picture_div) !=0:
            for i, image_link in enumerate(tqdm(image_links)):
                if image_link != "skip":
                    print("retrived %s link image: %s", i, image_link)
                    image_name = f"./{card_title}/{item_id}_{i}.jpg"
                    driver.get(image_link)            
                    time.sleep(1)
                    image_tag = driver.find_element(By.XPATH, value="//img")
                    with  open(image_name, "wb") as f:
                        f.write(image_tag.screenshot_as_png)
                    driver.back()

        else:
            raise "Cannot retrived any elements!!"

if __name__ == "__main__":
    initData()
    urls = load(INPUT_PATH)
    retrive(driver, urls)
