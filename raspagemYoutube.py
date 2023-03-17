from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import json
import time


def insert_the_disc_link(search_term):
    chrome = webdriver.Chrome(ChromeDriverManager().install())
    chrome.get("https://music.youtube.com/")

    search_button = chrome.find_element(By.CLASS_NAME, "ytmusic-search-box")

    search_button.click()

    search_input = chrome.find_element(By.TAG_NAME, "input")

    search_input.send_keys(search_term)
    search_input.send_keys(Keys.ENTER)
    time.sleep(2)
    try:
        disc = (
            chrome.find_element(By.TAG_NAME, "ytmusic-shelf-renderer")
            .find_element(By.TAG_NAME, "a")
            .get_attribute("href")
        )
    except:
        disc = "https://music.youtube.com/"
    return disc


def return_albuns_links():
    with open("discos.json", "r") as f:
        data = json.load(f)
        for disk in data:
            search_term = disk["title"] + " " + disk["artist"]
            disk["album_link"] = insert_the_disc_link(search_term)

    with open("discos.json", "w", encoding='utf8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


if __name__ == "__main__":
    return_albuns_links()
