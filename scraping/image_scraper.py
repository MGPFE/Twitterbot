from colorama import init, Fore, Style
from bs4 import BeautifulSoup
import threading
import requests
import sys
import os

# TODO REWRITE THE ENTIRE THING

# COLORAMA
init(convert=True)


class Image_Scraper:

    def __init__(self):

        self.real_list = list()
        self.bytes_list = list()
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
        content = r.content
        if content not in self.bytes_list and int(sys.getsizeof(content)) > 5000:
            self.bytes_list.append(content)
            with open(f"{str(file_name)}.jpeg", "wb") as f:
                f.write(content)

    def scrape(self, page):

        unsupported_ext = [
            "spacer", ".mp4", ".mov",
            "logo", ".gif"
        ]

        # while self.var <= 1:

        URL = page

        r = requests.get(URL)

        data = BeautifulSoup(r.text, "html.parser")

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

            # self.var += 1

        if self.real_list:

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

        else:
            input("\nCouldn't get any images...")
