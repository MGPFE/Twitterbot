from scraping.feed import Text_Scraper
from tqdm import tqdm
import sqlite3


class Db:

    def __init__(self):

        self.conn = sqlite3.connect('tweet.db')
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
        my_list = scraper.foodforbot()
        list_length = len(my_list)
        print('\nInserting data into database...')
        pbar = tqdm(total=list_length)
        for tw in range(list_length):
            self.c.execute("INSERT INTO tweets VALUES (?)", [my_list[tw]])
            self.conn.commit()
            pbar.update(1)

        pbar.close()
        print('Done!\n')

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
        # nr = self.c.fetchone()
        # print(nr[0])
        self.c.execute("DELETE FROM tweets WHERE tweet = (?)", (text, ))
        self.conn.commit()


# class User_db(Db):

#     def __init__(self):

#         self.conn = sqlite3.connect('tweet.db', check_same_thread=False)
#         self.c = self.conn.cursor()

#     def create_table(self):

#         self.c.execute("""CREATE TABLE IF NOT EXISTS i_follow (
#                 _id integer
#             )""")
#         self.conn.commit()

#     def insert(self, _id):

#         try:
#             for i in _id:
#                 self.c.execute("INSERT INTO i_follow VALUES (?)", (i,))
#         except TypeError:
#             self.c.execute("INSERT INTO i_follow VALUES (?)", (_id,))
#         self.conn.commit()

#     def fetch(self):

#         self.c.execute("SELECT * FROM i_follow")
#         items = self.c.fetchall()
#         self.conn.commit()
#         return items

#     # def count_entries(self):

#     #     self.c.execute("SELECT COUNT (*) FROM i_follow")
#     #     count = self.c.fetchone()
#     #     self.conn.commit()
#     #     return count[0]

#     def delete(self, del_id):

#         self.c.execute("SELECT _id FROM i_follow")
#         #print(nr[0])
#         self.c.execute("DELETE FROM i_follow WHERE _id = (?)", (del_id,))
#         self.conn.commit()
