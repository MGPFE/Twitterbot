from bs4 import BeautifulSoup
import threading
from tqdm import tqdm
import requests


class Text_Scraper:

    def __init__(self):

        self.var = 0
        self.quotes_set = set()

    def scrape(self):

        self.var += 1

        URL = (f'https://www.brainyquote.com/topics/daily-quotes_{str(self.var)}')

        page = requests.get(URL)

        soup = BeautifulSoup(page.content, 'html.parser')

        container = soup.find('div', id='quotesList')

        everything = container.find_all('div', class_='m-brick')

        for item in everything:
            if item.find(class_="clearfix"):
                raw_string = item.find(class_='clearfix')
                formatted_string = raw_string.text.strip().replace('\n', '~')
                quote_ready = formatted_string.split('~')
                if len(formatted_string) > 250:
                    continue
                else:
                    self.quotes_set.add(f'#motivation #quotes "{quote_ready[0]}" ~{quote_ready[1]}')

        self.pbar.update(1)

    def run_scraper(self):

        print('\nScraping...')
        self.pbar = tqdm(total=39)

        threads = []
        for _ in range(39):
            t = threading.Thread(target=self.scrape, args=())
            threads.append(t)
            t.start()

        for thread in threads:
            thread.join()

        self.pbar.close()
        print('Done!')
        return self.quotes_set
