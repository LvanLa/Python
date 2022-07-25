import time

import requests

from playwright.sync_api import sync_playwright

import os

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36"
}


class MusicDownload:
    def __init__(self, path, url):
        self.base_path = path
        self.url = url

    def download_music(self, page):
        name, url = self.get_music_name_url(page)
        res = requests.get(url, headers=headers)
        if res.status_code == 200:
            if not os.path.exists(self.base_path):
                os.mkdir(self.base_path)
            print(f"开始下载>>{name}")
            with open(f'{self.base_path}/{name}.mp4', "wb") as f:
                f.write(res.content)
            print(f"完成下载>>{name}")

    @staticmethod
    def get_music_name_url(page):
        # 获取音乐url
        elements = page.locator("audio[id='h5audio_media']")
        audio = elements.nth(0)
        src = audio.get_attribute("src")
        # 获取名称
        name = page.locator("[id='song_name'] a").text_content()
        return name, src

    def open_url(self, context):
        page = context.new_page()
        page.goto(self.url)
        time.sleep(5)
        return page

    def next_music(self, page):
        page.evaluate("()=>document.getElementsByClassName('btn_next')[0].click();")
        time.sleep(5)


if __name__ == '__main__':
    musicDownload = MusicDownload("D://music", "https://y.qq.com/portal/player_radio.html#id=167")
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        page = musicDownload.open_url(context)
        musicDownload.download_music(page)
        for i in range(10):
            musicDownload.next_music(page)
            musicDownload.download_music(page)
        page.close()
        browser.close()
