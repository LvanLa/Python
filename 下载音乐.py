import time

import requests
from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
import os

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36"
}

webdriver_path = "D:/ProgramFiles/chromedriver_win32/chromedriver.exe"


class MusicDownload:
    def __init__(self, path, url):
        self.base_path = path
        self.url = url

    def download_music(self, browser):
        name, url = self.get_music_name_url(browser)
        res = requests.get(url, headers=headers)
        if res.status_code == 200:
            if not os.path.exists(self.base_path):
                os.mkdir(self.base_path)

            with open(f'{self.base_path}/{name}.mp4', "wb") as f:
                f.write(res.content)

    @staticmethod
    def get_music_name_url(browser):
        # 获取音乐url
        element = browser.find_element(By.TAG_NAME, "audio")
        src = element.get_attribute("src")
        # 获取名称
        name = browser.find_element(By.ID, "song_name").find_element(By.TAG_NAME, "a").text
        return name, src

    def open_url(self):
        options = webdriver.ChromeOptions()
        options.add_argument("headless")
        browser = webdriver.Chrome(webdriver_path, chrome_options=options)
        browser.get(self.url)
        time.sleep(5)
        return browser

    def next_music(self, browser):
        el = browser.find_element(By.CSS_SELECTOR, "a.btn_next.js_play_next")
        browser.execute_script("arguments[0].click()", el)
        time.sleep(5)
        self.download_music(browser)


if __name__ == '__main__':
    musicDownload = MusicDownload("D://music", "https://y.qq.com/portal/player_radio.html#id=167")
    browser = musicDownload.open_url()
    musicDownload.download_music(browser)
    # for i in range(10):
    #     musicDownload.next_music(browser)
    # parse.parse_content(text)
