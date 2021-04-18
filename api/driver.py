from scraping.image_scraper import Image_Scraper
from scraping.databases import Db
from colorama import init, Fore, Style
import os
import threading
import time
import sys

# COLORAMA
init(convert=True)


class Driver:

    def __init__(
        self, karm, co_il, ile_l, related,
        s_fix, ile_foll, txt, img, wait_time,
        prev_tweets, reply_allow, bot
    ):
        self.karm = karm
        self.co_il = co_il
        self.ile_l = ile_l
        self.related = related
        self.s_fix = s_fix
        self.ile_foll = ile_foll
        self.txt = txt
        self.img = img
        self.wait_time = wait_time
        self.prev_tweets = prev_tweets
        self.allow_reply = reply_allow
        self.bot = bot
        self.i = 0

        if sys.platform == "win32":
            self.clear = "CLS"
        else:
            self.clear = "clear"

    def wait(self):

        after = (self.co_il / 60) / 60
        print(f"{Fore.CYAN}{self.bot.what_time()}{Style.RESET_ALL} -- Next action in {Fore.CYAN}{str(int(after))}{Style.RESET_ALL} hour/s! ({Fore.CYAN}{str(self.i)}{Style.RESET_ALL} tweet/s sent!)\n")
        time.sleep(self.co_il)

    def prnt_timeline(self):

        twts = self.bot.check_timeline(self.prev_tweets)
        for key, value in twts.items():
            if key == "username":
                pass
            else:
                print("")
                print(f"{Fore.CYAN}{twts['username']}{Style.RESET_ALL}:")
                print(value)

        input(f"\nPress {Fore.CYAN}ENTER{Style.RESET_ALL} to continue...")

    def load_database(self):

        if self.txt:
            # Dla wstawiania tekstu
            self.db = Db()
        ###############################################################
        # Pobieranie postow
            if self.karm:
                self.db.create_table()
                self.db.insert()
                print("Database populated!")
            else:
                self.db.create_table()

        # Ladowanie postow do tabeli
            # try:
            self.how_many = self.db.count_entries()

            if self.how_many == 0:
                print("\nDatabase is empty!")
                input(f"Press {Fore.CYAN}ENTER{Style.RESET_ALL} to return to main menu...")
                return False
            else:
                print(f"\nBot has {Fore.CYAN}{str(self.how_many)}{Style.RESET_ALL} posts in the database")
                try:
                    self.posty = self.db.fetch()
                except Exception as err:
                    print(f"{Fore.YELLOW}{err}{Style.RESET_ALL}")
                    return False
                else:
                    return True
        ###############################################################

        # Dla wstawiania samego obrazu
        ###############################################################
        elif self.img:
            # DEFINIOWANIE SCRAPERA OBRAZOW
            self.img_scraper = Image_Scraper()
            if self.karm:
                web_page = input("\nPlease input a link for images: ")
                self.img_scraper.foodforbot(web_page)

            else:
                try:
                    os.chdir("Files")
                except FileNotFoundError:
                    print(f"{Fore.YELLOW}\nYou don\'t have any images!{Style.RESET_ALL}")
                    return False
                else:
                    self.filenames = [name for name in os.listdir(".") if os.path.isfile(name)]
                    return True
        ###############################################################

    def run_threads(self, a_funcs):

        threads = [
            threading.Thread(target=self.bot.follow_back, args=(self.wait_time,)) if a_funcs[1] else None,  # Zaobserwuj followersow
            threading.Thread(target=self.bot.unfollow_v2, args=(self.wait_time,)) if a_funcs[2] else None,  # Odfollowuj osoby ktore cie nie obserwuja
            threading.Thread(target=self.bot.tweet_like, args=(
                self.ile_l,
                self.related,
                self.wait_time,
                self.allow_reply,
            )) if a_funcs[3] else None  # Lajkowanie tweetow tweetow (ile tweetow ma polajkowac, co ile sekund)
        ]

        for thread in threads:
            if thread is not None:
                thread.start()

        for thread in threads:
            if thread is not None:
                thread.join()

        # Zaobserwuj losowych uzytkownikow
        if a_funcs[4]:
            t4 = threading.Thread(target=self.bot.follow_random, args=(
                self.related,
                self.ile_foll,
                self.wait_time,
                self.allow_reply,
            ))

            t4.start()
            t4.join()

    def post_tweet(self, add_funcs):

        # Postowanie i like"owanie tweetow
        while self.i <= self.s_fix:          # bylo len(posty)
            try:
                if self.i == self.s_fix:
                    if self.txt:
                        self.db.close_db()
                        print("\nDatabase closed!")

                    else:
                        print("")

                    print("Done!")
                    input(f"\nPress {Fore.CYAN}ENTER{Style.RESET_ALL} to exit...")
                    sys.exit()

                if self.txt:
                    print("\nDo you want to send your own tweet or fetch some from the database?")
                    inp = input(f"Type {Fore.CYAN}OWN{Style.RESET_ALL} to send your own tweet: ").lower()
                    if inp == "own":
                        while True:
                            os.system(self.clear)
                            print("Please input your own tweet")
                            current_twt = input("\nInput your tweet: ")
                            if current_twt:
                                break
                            else:
                                input(f"\n{Fore.YELLOW}Type something!{Style.RESET_ALL}")
                    else:
                        for index, post in enumerate(self.posty, 1):
                            os.system(self.clear)
                            print("Pick a tweet to send")
                            print(f"\n{Fore.CYAN}Next tweet{Style.RESET_ALL}({index}/{self.how_many}): {post[0]}")
                            dec = input(f"\nType {Fore.CYAN}SEND{Style.RESET_ALL} to send it or press {Fore.CYAN}ENTER{Style.RESET_ALL} for next one: ").lower()
                            if dec == "send":
                                current_twt = post[0]
                                break

                    while True:
                        decision = input(f"\nDo you wish to send it? ({Fore.CYAN}Y{Style.RESET_ALL}/n): ")
                        actual_decision = decision.upper()
                        if actual_decision == "Y" or actual_decision == "":
                            sent = self.bot.post_tweet(current_twt, self.img, self.i)
                            break
                        elif actual_decision == "N":
                            sent = False
                            print("")
                            break

                elif self.img:
                    sent = self.bot.post_tweet(self.filenames[self.i], self.img, self.i)

                self.i += 1

                # W przypadku postowania wiecej niz jednego tweeta
                if self.s_fix > 1:
                    t0 = threading.Thread(target=self.wait)
                    t0.start()

                if sent:
                    # Usuń użytego posta z bazy danych
                    if self.txt:
                        self.db.delete(current_twt)

                    elif self.img:
                        self.img_scraper.delete_file(self.filenames[self.i - 1])

                if add_funcs[0]:
                    self.run_threads(add_funcs)

                if self.s_fix > 1:
                    print("\nThe bot is in standby mode!")
                    t0.join()

            except IndexError:
                if self.txt:
                    self.db.close_db()
                    print("\nDatabase closed!")

                else:
                    print("\n")

                print("Bot ran out of tweets, run a scraper!")
                input(f"\nPress {Fore.CYAN}ENTER{Style.RESET_ALL} to exit...")
                sys.exit()

            except KeyboardInterrupt:
                if self.txt:
                    self.db.close_db()
                    print("\nDatabase closed!")

                else:
                    print("\n")

                input(f"\nPress {Fore.CYAN}ENTER{Style.RESET_ALL} to exit...")
                sys.exit()

    def modular_cycle(self, sett):

        if sett[5]:

            DB_FLAG = self.load_database()

            if DB_FLAG:
                print(f"{Fore.YELLOW}\nWARNING! it is recommended NOT to close the bot manually!{Style.RESET_ALL}")
                self.prnt_timeline()

                self.post_tweet(sett)
            else:
                return
        else:
            self.prnt_timeline()
            while self.i <= self.s_fix:
                print("")
                if self.s_fix == self.i:
                    print("Done!")
                    input(f"\nPress {Fore.CYAN}ENTER{Style.RESET_ALL} to exit...")
                    sys.exit()

                if self.s_fix > 1:
                    t0 = threading.Thread(target=self.wait)
                    t0.start()

                self.run_threads(sett)
                self.i += 1

                if self.s_fix > 1:
                    print("\nThe bot is in standby mode!")
                    t0.join()

    def default_cycle(self, sett):

        DB_FLAG = self.load_database()

        if DB_FLAG:
            print(f"{Fore.YELLOW}\nWARNING! it is recommended NOT to close the bot manually!{Style.RESET_ALL}")
            self.prnt_timeline()

            self.post_tweet(sett)
        else:
            return


if __name__ == "__main__":

    driver = Driver(
        None, None, None, None,
        None, None, None, None,
        None, None, None, None
    )
    # driver.authinput()
