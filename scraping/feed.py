from bs4 import BeautifulSoup
import concurrent.futures
from tqdm import tqdm
import requests
import os


class Text_Scraper:

    def __init__(self):

        self.var = 0
        self.real_list = []

    def scrape(self):

        self.var += 1

        URL = (f'https://www.brainyquote.com/topics/daily-quotes_{str(self.var)}')

        page = requests.get(URL)

        soup = BeautifulSoup(page.content, 'html.parser')

        container = soup.find('div', id='quotesList')

        everything = container.find_all('div', class_='m-brick')

        for item in everything:
            quote_itself = item.find(class_='clearfix')
            quote_almost_ready = quote_itself.text.strip().replace('\n\n', '~')
            quote_ready = quote_almost_ready.split('~')
            if len(quote_almost_ready) > 250:
                continue
            else:
                self.real_list.append(f'#motivation #quotes "{quote_ready[0]}" ~{quote_ready[1]}')

        self.pbar.update(1)

    def foodforbot(self):

        print('\nScraping...')
        self.pbar = tqdm(total=39)

        with concurrent.futures.ThreadPoolExecutor() as executor:
            _ = [executor.submit(self.scrape) for _ in range(39)]

        self.pbar.close()
        print('Done!')
        return self.real_list
