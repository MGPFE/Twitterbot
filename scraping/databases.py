from scraping.text_scraper import Text_Scraper
from tqdm import tqdm
import sqlite3


class Db:

    def __init__(self):

        self.conn = sqlite3.connect("tweet.db")
        self.c = self.conn.cursor()
        self.create_table()

    def create_table(self):

        self.c.execute("""CREATE TABLE IF NOT EXISTS tweets (
                tweet text
            )""")
        self.conn.commit()

    def close_db(self):

        self.conn.close()

    def insert(self):

        scraper = Text_Scraper()
        my_set = scraper.run_scraper()
        set_length = len(my_set)
        print("\nInserting data into database...")
        pbar = tqdm(total=set_length)
        for i in range(set_length):
            self.c.execute("INSERT INTO tweets VALUES (?)", (my_set.pop(),))
            self.conn.commit()
            pbar.update(1)

        pbar.close()
        print("Done!\n")

    def new_entry(self, entry):

        self.c.execute("INSERT INTO tweets VALUES (?)", (entry,))
        self.conn.commit()

    def fetch(self):

        self.c.execute("SELECT * FROM tweets")
        items = self.c.fetchall()
        self.conn.commit()
        return items

    def count_entries(self):

        self.c.execute("SELECT COUNT (*) FROM tweets")
        count = self.c.fetchone()
        self.conn.commit()
        return count[0]

    def delete(self, text):

        self.c.execute("SELECT tweet FROM tweets")
        self.c.execute("DELETE FROM tweets WHERE tweet = (?)", (text,))
        self.conn.commit()
