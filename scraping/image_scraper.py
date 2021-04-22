from colorama import init, Fore, Style
from selenium import webdriver
from bs4 import BeautifulSoup
from io import BytesIO
from PIL import Image
import threading
import requests
import os

# COLORAMA
init(convert=True)


class Image_Scraper:

    def __init__(self):

        self.real_list = []
        self.var = 1
        self.i = 0

    def delete_file(self, name):

        os.remove(name)

    def create_folder(self):

        dir = os.path.join("Files")

        if not os.path.exists(dir):
            os.mkdir(dir)

        os.chdir("Files")

    def download_image(self, URL, file_name):

        r = requests.get(URL)
        im = Image.open(BytesIO(r.content))
        im.save(str(file_name) + ".jpg")

    def foodforbot(self, page):

        browser = webdriver.Chrome()

        unsupported_ext = [
            "spacer", ".png", ".jpeg",
            ".mp4", ".mov", "logo", ".gif"
        ]

        while self.var <= 1:

            URL = page

            browser.get(URL)

            data = BeautifulSoup(browser.page_source, "html.parser")

            try:

                for src in data.find_all("img"):

                    if len(self.real_list) >= 200:
                        break

                    for ext in unsupported_ext:
                        if ext in src["src"]:
                            continue

                    self.real_list.append(src["src"])

            except KeyError:
                print(f"\n{Fore.RED}Couldn\'t download any images from this page!{Style.RESET_ALL}")
                return

            self.var += 1

        self.create_folder()

        threads = []

        for item in self.real_list:

            t = threading.Thread(target=self.download_image, args=(item, self.i))
            try:
                t.start()
                threads.append(t)
            except Exception as e:
                pass
            self.i += 1

        for thread in threads:
            thread.join()

        browser.close()
