from colorama import init, Fore, Style
from configparser import ConfigParser
from api.twitterbot import Twitterbot
from misc.misc_funcs import email_err, check_os
from api.driver import Driver
from scraping.databases import Db
import platform
import time
import sys
import os

# COLORAMA
init(convert=True)


class Main:

    def __init__(self):
        self.version = {
            "ver": "1.3.9",
            "date": "2.07.2021",
            "time": "8:53"
        }
        self.create_config()
        self.set_vars()
        self.clear = check_os()

    def create_config(self):
        # CONFIG FILE
        self.config = ConfigParser()

        botconfig = {
            "text": "True", "image": "False", "howOften": "14400",
            "likes": "10", "reply_allowed": "True", "follows": "5",
            "relation": "python", "waittime": "10", "prevtweets": "3",
            "mode": "0", "senderrors": "True", "modular": "False",
            "follow_back": "True", "unfollow": "True",
            "tweet_like": "True", "follow_random": "True",
            "send_tweet": "True", "display_ver": "False"
        }

        # CREATE CONFIG IF DOESN"T EXIST
        if not os.path.exists("config.ini"):
            self.config.add_section("Theme")
            self.config.add_section("BotConfig")
            self.config.add_section("LoginData")
            self.config["Theme"]["current"] = "0"

            for k, v in botconfig.items():
                self.config["BotConfig"][k] = v

            self.config["LoginData"]["apikey"] = "None"
            self.config["LoginData"]["apisecretkey"] = "None"
            self.config["LoginData"]["accesstoken"] = "None"
            self.config["LoginData"]["accesstokensecret"] = "None"

            # SAVE TO CONFIG
            try:
                with open("config.ini", "w") as f:
                    self.config.write(f)
            except Exception:
                self.CONFIG_CREATED = False
            else:
                self.CONFIG_CREATED = True

        else:
            self.CONFIG_CREATED = True

        # READ FROM CONFIG
        if self.CONFIG_CREATED:
            self.config.read("config.ini")

    def set_config(self, parent, child, value):

        if self.CONFIG_CREATED:
            self.config.set(parent, child, value)

            with open("config.ini", "w") as f:
                self.config.write(f)
        else:
            return

    def set_vars(self):

        if self.CONFIG_CREATED:
            # LOAD CONFIG VALUES IF EXISTS
            # Themes
            self.themetab = [Fore.CYAN, Fore.BLUE, Fore.MAGENTA, Fore.WHITE]
            self.theme = self.themetab[self.config.getint("Theme", "current")]
            # Help
            self.AUTHORIZED = False
            self.t_bot = None
            # Bot config (MAIN)
            self.text = self.config.getboolean("BotConfig", "text")
            self.image = self.config.getboolean("BotConfig", "image")
            self.co_ile = self.config.getint("BotConfig", "howOften")
            self.karmienie = False
            self.ile_lajk = self.config.getint("BotConfig", "likes")
            self.reply_allow = self.config.getboolean(
                "BotConfig",
                "reply_allowed"
            )
            self.ile_follow = self.config.getint("BotConfig", "follows")
            self.related_to = self.config.get("BotConfig", "relation")
            self.wait_time_conv = self.config.get("BotConfig", "waittime")
            self.prev_tweets_conv = self.config.get("BotConfig", "prevtweets")
            self.mode = self.config.getint("BotConfig", "mode")
            self.send_errors = self.config.getboolean(
                "BotConfig",
                "senderrors"
            )
            self.modular = self.config.getboolean("BotConfig", "modular")
            self.follow_back = self.config.getboolean(
                "BotConfig",
                "follow_back"
            )
            self.unfollow = self.config.getboolean("BotConfig", "unfollow")
            self.tweet_like = self.config.getboolean("BotConfig", "tweet_like")
            self.follow_random = self.config.getboolean(
                "BotConfig",
                "follow_random"
            )
            self.tweet_send = self.config.getboolean("BotConfig", "send_tweet")
            self.DISPLAY_VER = self.config.getboolean(
                "BotConfig",
                "display_ver"
            )
            self.authtab = [
                self.config.get("LoginData", "apikey"),
                self.config.get("LoginData", "apisecretkey"),
                self.config.get("LoginData", "accesstoken"),
                self.config.get("LoginData", "accesstokensecret")
            ]

        else:
            # DEFAULT VARS IF CONFIG DOESN'T EXIST
            # Themes
            self.themetab = [Fore.CYAN, Fore.BLUE, Fore.MAGENTA, Fore.WHITE]
            self.theme = self.themetab[0]
            # Help
            self.AUTHORIZED = False
            self.t_bot = None
            # Bot config (MAIN)
            self.text = True
            self.image = False
            self.co_ile = 10
            self.karmienie = False
            self.ile_lajk = 10
            self.reply_allow = True
            self.ile_follow = 5
            self.related_to = "python"
            self.wait_time_conv = 10
            self.prev_tweets_conv = 3
            self.mode = 0
            self.send_errors = True
            self.modular = False
            self.follow_back = True
            self.unfollow = True
            self.tweet_like = True
            self.follow_random = True
            self.tweet_send = True
            self.DISPLAY_VER = False
            self.authtab = []

    def authinput(self):

        names = [
            "API key", "API secret key",
            "Access token", "Access token secret"
        ]
        authtable = []
        print(f"Please input your {self.theme}validation codes{Style.RESET_ALL}")
        print(f"(You can press {self.theme}ENTER{Style.RESET_ALL} if you don\'t have them)")
        print(f"(Validation codes can be found at {self.theme}https://developer.twitter.com{Style.RESET_ALL})")
        for index, key in enumerate(names):
            code = input(f"{self.theme}{key}{Style.RESET_ALL}: ")
            if index == 0 and code == "":
                break
            else:
                authtable.append(code)
        print("")
        return authtable

    def create_bot(self):

        try:

            if self.authtab[0] == "None":
                # TEMPORARY TABLE THAT KEEPS authtab[0] AT NONE
                temp_tab = self.authinput()
                if len(temp_tab) == 0:
                    return False
                else:
                    # IF INPUT IS NOT NONE THEN INPUT INTO temp_tab
                    self.authtab = temp_tab

            self.t_bot = Twitterbot(
                self.authtab[0],
                self.authtab[1],
                self.authtab[2],
                self.authtab[3]
            )

        except Exception:
            self.authtab[0] = "None"
            pass

        else:
            # INPUT ACCESS KEYS INTO CONFIG
            if self.CONFIG_CREATED:
                names = [
                    "apikey", "apisecretkey",
                    "accesstoken", "accesstokensecret"
                ]
                for index, name in enumerate(names):
                    self.config.set("LoginData", name, f"{self.authtab[index]}")
                with open("config.ini", "w") as f:
                    self.config.write(f)
            input(f"\nPress {self.theme}ENTER{Style.RESET_ALL} to continue...")
            return True

    def mainloop(self):

        os.system(self.clear)

        # INPUT ACCESS KEYS
        self.AUTHORIZED = self.create_bot()

        # MAINLOOP
        while True:

            os.system(self.clear)

            print(f"|{self.theme}Twitterbot{Style.RESET_ALL} {Fore.BLACK}{Style.BRIGHT}{self.version.get('ver')}{Style.RESET_ALL}") if self.DISPLAY_VER else print(f"|{self.theme}Twitterbot{Style.RESET_ALL}")
            print(f"|Connection status: {f'{Fore.GREEN}Connected{Style.RESET_ALL}' if self.AUTHORIZED else f'{Fore.RED}Not connected!{Style.RESET_ALL}'}")
            print(end=" \t\t\t\t")
            print(f"|{self.theme}Current settings{Style.RESET_ALL}:")
            print("|1. Start it up!", end="\t\t")
            print(f"|Relations: {self.theme}{self.related_to}{Style.RESET_ALL}", end="\t")
            print(f"|Posting interval: {self.theme}{int((self.co_ile/60)/60)}h{Style.RESET_ALL}")
            print("|2. Edit options", end="\t\t")
            print(f"|People to follow: {self.theme}{self.ile_follow}{Style.RESET_ALL}", end="\t")
            print(f"|Feed the bot: {self.theme}{self.karmienie}{Style.RESET_ALL}")
            print("|3. Exit Program", end="\t\t")
            print(f"|Tweets to like: {self.theme}{self.ile_lajk}{Style.RESET_ALL}", end="\t")
            print(f"|Wait: {self.theme}{self.wait_time_conv}s{Style.RESET_ALL}")
            print(end="\t\t\t\t")
            print(f"|Text or Image: {self.theme}{'Text' if self.text else 'Image'}{Style.RESET_ALL}", end="\t")
            print(f"|Previous Tweets: {self.theme}{self.prev_tweets_conv}{Style.RESET_ALL}")
            print(end="\t\t\t\t")
            print(f"|Reply allowed: {self.theme}{self.reply_allow}{Style.RESET_ALL}", end="\t")
            print(f"|Modularity: {self.theme}{self.modular}{Style.RESET_ALL}")
            wybor = input(f"{self.theme}Choice{Style.RESET_ALL}: ")

            # START IT UP
            if wybor == "1":
                msg = "How many tweets to post" if self.tweet_send or not self.modular else "How many times to repeat the cycle"
                while True:

                    fix = input(f"\n{msg}: ")

                    try:
                        fix_int = int(fix)
                        break

                    except ValueError:
                        print(f"{Fore.RED}The value couldn\'t be converted into an integer{Style.RESET_ALL}")
                        input(f"Press {self.theme}ENTER{Style.RESET_ALL} to try again...")

                if not self.AUTHORIZED:
                    while True:
                        print("")
                        helpful_var = self.create_bot()
                        if not helpful_var:
                            input(f"{Fore.RED}Couldn\'t authorize{Style.RESET_ALL}, press {self.theme}ENTER{Style.RESET_ALL} to try again...")
                        else:
                            break

                if self.mode == 0:
                    driver = Driver(
                        self.karmienie, self.co_ile, self.ile_lajk,
                        self.related_to, fix_int, self.ile_follow, self.text,
                        self.image, self.wait_time_conv, self.prev_tweets_conv,
                        self.reply_allow, self.t_bot
                    )

                    if self.modular:
                        settings = [
                            self.modular, self.follow_back,
                            self.unfollow, self.tweet_like,
                            self.follow_random, self.tweet_send
                        ]
                        driver.modular_cycle(settings)
                    else:
                        settings = [True for _ in range(6)]
                        driver.default_cycle(settings)

            # EDIT OPTIONS
            elif wybor == "2":
                while True:
                    os.system(self.clear)

                    print("Options")
                    print(f"\n|{self.theme}Bot setup{Style.RESET_ALL}:", end="\t\t\t")
                    print(f"|{self.theme}Customization{Style.RESET_ALL}:")
                    if self.AUTHORIZED:
                        print("\n1. Scraper/Mode", end="\t\t\t")
                        print("7. Account settings")
                    else:
                        print("\n1. Scraper/Mode")
                    print("2. How long to wait", end="\t\t")
                    print("8. Main menu theme")
                    print("3. Tweet/DM settings")
                    print("4. Set relations")
                    print("5. Users-follow count")
                    print("6. Other")
                    print("\n9. Go back")
                    wybor2 = input(f"\n{self.theme}Choice{Style.RESET_ALL}: ")

                    # SCRAPER / MODE
                    if wybor2 == "1":
                        while True:
                            os.system(self.clear)

                            print("Scraper/Mode settings")
                            print("\n1. Tweeting mode")
                            print("2. Scrape the web")
                            print("3. Cycle settings")
                            print("\n4. Go back")
                            wybor0 = input(f"\n{self.theme}Choice{Style.RESET_ALL}: ")

                            # WHAT SCRAPER/MODE TO USE
                            if wybor0 == "1":
                                os.system(self.clear)

                                print("What scraper to use")
                                print("\n1. Text scraper (One webpage only)")
                                print("2. Image scraper (BETA)")
                                wybor7 = input(f"\n{self.theme}Choice{Style.RESET_ALL}: ")

                                # TEXT SCRAPER
                                if wybor7 == "1":
                                    # WRITE TO CONFIG FILE
                                    if self.CONFIG_CREATED:
                                        self.config.set("BotConfig", "text", "True")
                                        self.config.set("BotConfig", "image", "False")
                                        with open("config.ini", "w") as f:
                                            self.config.write(f)

                                    print("\nThe bot will use a text scraper!")
                                    time.sleep(1)
                                    self.text = True
                                    self.image = False

                                # IMAGE SCRAPER
                                elif wybor7 == "2":
                                    # WRITE TO CONFIG FILE
                                    if self.CONFIG_CREATED:
                                        self.config.set("BotConfig", "text", "False")
                                        self.config.set("BotConfig", "image", "True")
                                        with open("config.ini", "w") as f:
                                            self.config.write(f)

                                    print("\nThe bot will use an image scraper!")
                                    time.sleep(1)
                                    self.text = False
                                    self.image = True

                            # FEED THE BOT
                            elif wybor0 == "2":
                                os.system(self.clear)

                                print("Do you want to scrape the web?")
                                print("\n1. Yes")
                                print("2. No")
                                wybor3 = input(f"\n{self.theme}Choice{Style.RESET_ALL}: ")

                                # YES
                                if wybor3 == "1":
                                    print("\nBot will scrape the web during runtime!")
                                    self.karmienie = True
                                    time.sleep(1)

                                # NO
                                elif wybor3 == "2":
                                    self.karmienie = False

                            # CYCLE SETTINGS
                            elif wybor0 == "3":
                                os.system(self.clear)

                                print("Cycle settings")
                                print("\n1. Regular mode")
                                print("2. Infinite mode")
                                wybor10 = input(f"\n{self.theme}Choice{Style.RESET_ALL}: ")

                                # REGULAR MODE
                                if wybor10 == "1":
                                    self.set_config("BotConfig", "mode", "0")
                                    self.mode = 0

                                # INFINITE MODE
                                elif wybor10 == "2":
                                    self.set_config("BotConfig", "mode", "1")
                                    self.mode = 1

                            elif wybor0 == "4":
                                break

                    # HOW LONG TO WAIT BETWEEN TWEETS
                    elif wybor2 == "2":

                        while True:
                            os.system(self.clear)
                            print("How long to wait after the bot is done with it\'s procedures")
                            print(f"(RECOMMENDED: {self.theme}4h{Style.RESET_ALL})")
                            wybor4 = input("\nInput a number: ")

                            try:
                                converted = int(wybor4)
                            except ValueError:
                                print(f"{Fore.RED}The value couldn\'t be converted into an integer{Style.RESET_ALL}")
                                input(f"Press {self.theme}ENTER{Style.RESET_ALL} to try again")
                            else:
                                self.co_ile = (converted * 60) * 60
                                # WRITE TO CONFIG FILE
                                self.set_config("BotConfig", "howOften", f"{self.co_ile}")

                                print(f"\nThe interval has been set to {self.theme}{converted}h{Style.RESET_ALL}")
                                time.sleep(1)
                                break

                    # HOW MANY TWEETS TO LIKE
                    elif wybor2 == "3":
                        while True:

                            os.system(self.clear)

                            print("Tweet/DM settings")
                            print("\n1. How many tweets to like")
                            print(f"2. Reply to tweets/DM\'s ({self.theme}{self.reply_allow}{Style.RESET_ALL})")
                            print("\n3. Go back")
                            wybor5 = input(f"\n{self.theme}Choice{Style.RESET_ALL}: ")

                            if wybor5 == "1":
                                os.system(self.clear)
                                print("How many tweets to like")
                                print(f"(RECOMMENDED: {self.theme}10{Style.RESET_ALL})")
                                conv = input("\nInput a number: ")

                                try:
                                    self.ile_lajk = int(conv)

                                    # WRITE TO CONFIG FILE
                                    self.set_config("BotConfig", "likes", f"{self.ile_lajk}")

                                except ValueError:
                                    print(f"{Fore.RED}The value couldn\'t be converted into an integer{Style.RESET_ALL}")
                                    time.sleep(1)

                                else:
                                    print(f"\nBot will like {self.theme}{self.ile_lajk}{Style.RESET_ALL} tweets!")
                                    time.sleep(1)

                            elif wybor5 == "2":
                                os.system(self.clear)
                                print("Reply to tweets/DM\'s")
                                print("\n1. True")
                                print("2. False")
                                rep = input(f"\n{self.theme}Choice{Style.RESET_ALL}: ")

                                if rep == "1":
                                    self.reply_allow = True
                                elif rep == "2":
                                    self.reply_allow = False

                                print(f"\nReply functionality set to {self.theme}{self.reply_allow}{Style.RESET_ALL}")
                                time.sleep(1)

                                self.set_config("BotConfig", "reply_allowed", f"{self.reply_allow}")

                            elif wybor5 == "3":
                                break

                    # FOLLOW PEOPLE AND LIKE TWEETS RELATED TO
                    elif wybor2 == "4":
                        os.system(self.clear)

                        print("Set relations")
                        self.related_to = input("\nFollow people and like tweets related to: ")

                        # WRITE TO CONFIG FILE
                        self.set_config("BotConfig", "relation", f"{self.related_to}")

                        print(f"\nBot will follow people related to {self.theme}{self.related_to}{Style.RESET_ALL}!")
                        time.sleep(1)

                    # HOW MANY PEOPLE TO FOLLOW
                    elif wybor2 == "5":
                        while True:

                            os.system(self.clear)

                            print("How many users to follow")
                            print(f"(RECOMMENDED: {self.theme}5{Style.RESET_ALL})")
                            wybor6 = input("\nInput number: ")

                            try:
                                self.ile_follow = int(wybor6)

                                # WRITE TO CONFIG FILE
                                self.set_config("BotConfig", "follows", f"{self.ile_follow}")

                            except ValueError:
                                print(f"{Fore.RED}The value couldn\'t be converted into an integer{Style.RESET_ALL}")
                                input(f"Press {self.theme}ENTER{Style.RESET_ALL} to try again")

                            else:
                                print(f"\nBot will follow {self.theme}{self.ile_follow}{Style.RESET_ALL} people!")
                                time.sleep(1)
                                break

                    elif wybor2 == "6":
                        while True:
                            os.system(self.clear)
                            print("Other")
                            print("\n1. How long to wait between likes/follows")
                            print("2. How many previous tweets to display")
                            print("3. Send error data")
                            print("4. Modular settings")
                            print("5. Bot info")
                            print("6. View database")
                            print("\n7. Go back")
                            oth = input(f"\n{self.theme}Choice{Style.RESET_ALL}: ")

                            if oth == "1":
                                os.system(self.clear)
                                print("How long to wait between likes/follows etc.")
                                print(f"(RECOMMENDED: {self.theme}10{Style.RESET_ALL} seconds)")
                                wait_time = input("\nInput a number: ")
                                try:
                                    self.wait_time_conv = int(wait_time)
                                except ValueError:
                                    print(f"\n{Fore.RED}Please insert an integer value!{Style.RESET_ALL}")
                                    time.sleep(1)
                                else:
                                    print(f"\nTime has been set to {self.theme}{self.wait_time_conv}{Style.RESET_ALL} seconds!")
                                    # Save to config file
                                    self.set_config("BotConfig", "waittime", f"{self.wait_time_conv}")

                                    time.sleep(1)

                            elif oth == "2":
                                os.system(self.clear)
                                print("How many previous tweets to display")
                                print(f"(RECOMMENDED: {self.theme}3{Style.RESET_ALL})")
                                prev_tweets = input("\nInput a number: ")
                                try:
                                    while True:
                                        self.prev_tweets_conv = int(prev_tweets)
                                        if self.prev_tweets_conv <= 10:
                                            break
                                        else:
                                            print(f"{Fore.YELLOW}Your input was {prev_tweets} while the limit is 10!{Style.RESET_ALL}")
                                except ValueError:
                                    print(f"\n{Fore.RED}Please insert an integer value!{Style.RESET_ALL}")
                                    time.sleep(1)
                                else:
                                    print(f"\nBot will display {self.theme}{self.prev_tweets_conv}{Style.RESET_ALL} of your previous tweets!")
                                    # Save to config file
                                    self.set_config("BotConfig", "prevtweets", f"{self.prev_tweets_conv}")

                                    time.sleep(1)

                            elif oth == "3":
                                os.system(self.clear)
                                print("Send error data")
                                print(f"(RECOMMENDED: {self.theme}TRUE{Style.RESET_ALL})")
                                print("\n1. True")
                                print("2. False")
                                err_data = input(f"\n{self.theme}Choice{Style.RESET_ALL}: ")

                                if err_data == "1":
                                    self.send_errors = True
                                    self.set_config("BotConfig", "senderrors", "True")
                                    print("\nThe bot will send error data!")
                                    time.sleep(1)
                                elif err_data == "2":
                                    self.send_errors = False
                                    self.set_config("BotConfig", "senderrors", "False")
                                    print("\nThe bot will not send error data!")
                                    time.sleep(1)

                            elif oth == "4":
                                while True:
                                    os.system(self.clear)

                                    print("Modular settings")
                                    print(f"\n1. Turned on ({self.theme}{self.modular}{Style.RESET_ALL})")
                                    if self.modular:
                                        print(f"2. Follow back ({self.theme}{self.follow_back}{Style.RESET_ALL})")
                                        print(f"3. Unfollow ({self.theme}{self.unfollow}{Style.RESET_ALL})")
                                        print(f"4. Like tweets ({self.theme}{self.tweet_like}{Style.RESET_ALL})")
                                        print(f"5. Follow random people ({self.theme}{self.follow_random}{Style.RESET_ALL})")
                                        print(f"6. Send new tweet ({self.theme}{self.tweet_send}{Style.RESET_ALL})")
                                    print("\n7. Go back")
                                    oth3 = input(f"\n{self.theme}Choice{Style.RESET_ALL}: ")

                                    if oth3 == "1":
                                        os.system(self.clear)
                                        print("Turn on or off")
                                        print("\n1. On")
                                        print("2. Off")
                                        oth4 = input(f"\n{self.theme}Choice{Style.RESET_ALL}: ")

                                        if oth4 == "1":
                                            self.modular = True
                                        elif oth4 == "2":
                                            self.modular = False

                                        print(f"\nModular settings set to {self.theme}{self.modular}{Style.RESET_ALL}!")
                                        time.sleep(1)

                                        self.set_config("BotConfig", "modular", f"{self.modular}")

                                    if oth3 == "2":
                                        if self.modular:
                                            os.system(self.clear)
                                            print("Follow back your followers")
                                            print("\n1. True")
                                            print("2. False")
                                            oth4 = input(f"\n{self.theme}Choice{Style.RESET_ALL}: ")

                                            if oth4 == "1":
                                                self.follow_back = True
                                            elif oth4 == "2":
                                                self.follow_back = False

                                            print(f"\nFollow back set to {self.theme}{self.follow_back}{Style.RESET_ALL}!")
                                            time.sleep(1)

                                            self.set_config("BotConfig", "follow_back", f"{self.follow_back}")

                                    if oth3 == "3":
                                        if self.modular:
                                            os.system(self.clear)
                                            print("Unfollow people that are not following you")
                                            print("\n1. True")
                                            print("2. False")
                                            oth4 = input(f"\n{self.theme}Choice{Style.RESET_ALL}: ")

                                            if oth4 == "1":
                                                self.unfollow = True
                                            elif oth4 == "2":
                                                self.unfollow = False

                                            print(f"\nUnfollow set to {self.theme}{self.unfollow}{Style.RESET_ALL}!")
                                            time.sleep(1)

                                            self.set_config("BotConfig", "unfollow", f"{self.unfollow}")

                                    if oth3 == "4":
                                        if self.modular:
                                            os.system(self.clear)
                                            print("Like random tweets")
                                            print("\n1. True")
                                            print("2. False")
                                            oth4 = input(f"\n{self.theme}Choice{Style.RESET_ALL}: ")

                                            if oth4 == "1":
                                                self.tweet_like = True
                                            elif oth4 == "2":
                                                self.tweet_like = False

                                            print(f"\nLike random tweets set to {self.theme}{self.tweet_like}{Style.RESET_ALL}!")
                                            time.sleep(1)

                                            self.set_config("BotConfig", "tweet_like", f"{self.tweet_like}")

                                    if oth3 == "5":
                                        if self.modular:
                                            os.system(self.clear)
                                            print("Follow random people")
                                            print("\n1. True")
                                            print("2. False")
                                            oth4 = input(f"\n{self.theme}Choice{Style.RESET_ALL}: ")

                                            if oth4 == "1":
                                                self.follow_random = True
                                            elif oth4 == "2":
                                                self.follow_random = False

                                            print(f"\nUnfollow set to {self.theme}{self.follow_random}{Style.RESET_ALL}!")
                                            time.sleep(1)

                                            self.set_config("BotConfig", "follow_random", f"{self.follow_random}")

                                    if oth3 == "6":
                                        if self.modular:
                                            os.system(self.clear)
                                            print("Send new tweet")
                                            print("\n1. True")
                                            print("2. False")
                                            oth4 = input(f"\n{self.theme}Choice{Style.RESET_ALL}: ")

                                            if oth4 == "1":
                                                self.tweet_send = True
                                            elif oth4 == "2":
                                                self.tweet_send = False

                                            print(f"\nSend new tweet set to {self.theme}{self.tweet_send}{Style.RESET_ALL}!")
                                            time.sleep(1)

                                            self.set_config("BotConfig", "send_tweet", f"{self.tweet_send}")

                                    elif oth3 == "7":
                                        break

                            elif oth == "5":
                                os.system(self.clear)
                                print("Bot info")
                                if self.AUTHORIZED:
                                    print(self.t_bot)
                                    print(f"Twitterbot version: {self.theme}{self.version.get('ver')}{Style.RESET_ALL} ({self.version.get('date')} - {self.version.get('time')})")
                                    print(f"Python version: {self.theme}{platform.python_version()}{Style.RESET_ALL} {platform.python_build()}")
                                    print(f"OS: {self.theme}{platform.system()} {platform.release()}{Style.RESET_ALL} - {platform.version()}")
                                    print("\n1. Change validation codes")
                                    print("2. Display Twitterbot version on main screen")
                                    oth2 = input(f"\n{self.theme}Choice{Style.RESET_ALL}: ")

                                    if oth2 == "1":
                                        print("\nYou will be relogged!")
                                        time.sleep(1)
                                        os.system(self.clear)
                                        self.authtab[0] = "None"
                                        self.create_bot()

                                    elif oth2 == "2":
                                        os.system(self.clear)
                                        print("Display Twitterbot version on main screen")
                                        print("\n1. True")
                                        print("2. False")
                                        disp = input(f"\n{self.theme}Choice{Style.RESET_ALL}: ")

                                        if disp == "1":
                                            print("\nTwitterbot version will be displayed on main screen!")
                                            self.set_config("BotConfig", "display_ver", "True")
                                            self.DISPLAY_VER = True
                                            time.sleep(1)

                                        elif disp == "2":
                                            print("\nTwitterbot version will not be displayed on main screen!")
                                            self.set_config("BotConfig", "display_ver", "False")
                                            self.DISPLAY_VER = False
                                            time.sleep(1)
                                else:
                                    print(f"\nTwitterbot version: {self.theme}{self.version.get('ver')}{Style.RESET_ALL} ({self.version.get('date')} - {self.version.get('time')})")
                                    print(f"Python version: {self.theme}{platform.python_version()}{Style.RESET_ALL} {platform.python_build()}")
                                    print(f"OS: {self.theme}{platform.system()} {platform.release()}{Style.RESET_ALL} - {platform.version()}")
                                    print("\n1. Display Twitterbot version on main screen")
                                    oth3 = input(f"\n{self.theme}Choice{Style.RESET_ALL}: ")

                                    if oth3 == "1":
                                        os.system(self.clear)
                                        print("Display Twitterbot version on main screen")
                                        print("\n1. True")
                                        print("2. False")
                                        disp = input(f"\n{self.theme}Choice{Style.RESET_ALL}: ")

                                        if disp == "1":
                                            print("\nTwitterbot version will be displayed on main screen!")
                                            self.set_config("BotConfig", "display_ver", "True")
                                            self.DISPLAY_VER = True
                                            time.sleep(1)

                                        elif disp == "2":
                                            print("\nTwitterbot version will not be displayed on main screen!")
                                            self.set_config("BotConfig", "display_ver", "False")
                                            self.DISPLAY_VER = False
                                            time.sleep(1)

                            elif oth == "6":

                                data = Db()
                                data.create_table()

                                os.system(self.clear)
                                print("Database options")
                                print("\nDo you wish to view your database contents or add to it?")

                                inp = input(f"Type {Fore.CYAN}VIEW{Style.RESET_ALL} or {Fore.CYAN}ADD{Style.RESET_ALL}: ").lower()
                                if inp == "view":
                                    if data.count_entries() != 0:
                                        tweets = data.fetch()

                                        for index in range(data.count_entries()):
                                            os.system(self.clear)
                                            print("Database contents")
                                            print(f"(click {self.theme}ENTER{Style.RESET_ALL} to view next one, type {self.theme}EXIT{Style.RESET_ALL} to go back or {self.theme}D{Style.RESET_ALL} to delete record)\n")

                                            tweet = tweets[index]
                                            print(f"({self.theme}{(index + 1)}{Style.RESET_ALL} / {len(tweets)})")
                                            print(f"{tweet[0]}")

                                            decision = input(f"\n{self.theme}Choice{Style.RESET_ALL}: ")
                                            actual_decision = decision.upper()

                                            if actual_decision == "":
                                                continue
                                            elif actual_decision == "D":
                                                sure = input(f"{Fore.YELLOW}Are you sure? (Y/n): {Style.RESET_ALL}")
                                                actual_sure = sure.upper()
                                                if actual_sure == "Y" or actual_sure == "":
                                                    data.delete(tweet[0])
                                                else:
                                                    pass
                                            elif actual_decision == "EXIT":
                                                break
                                            else:
                                                continue

                                    else:
                                        os.system(self.clear)
                                        print("Database contents")
                                        input("\nYour database is empty!")

                                elif inp == "add":
                                    os.system(self.clear)
                                    print("Add to database")
                                    new_entry = input("\nNew entry: ")

                                    if new_entry:
                                        while True:
                                            decision = input(f"\nDo you wish to add it? ({Fore.CYAN}Y{Style.RESET_ALL}/n): ").lower()
                                            if decision == "y" or decision == "":
                                                data.new_entry(new_entry)
                                                break
                                            elif decision == "n":
                                                print("")
                                                break
                                    else:
                                        print(f"\n{Fore.YELLOW}You didn\'t type anything!{Style.RESET_ALL}")
                                        time.sleep(1)

                            elif oth == "7":
                                break

                    # CUSTOMIZATION / ACCOUNT SETTINGS

                    elif wybor2 == "7":
                        if self.AUTHORIZED:
                            while True:
                                os.system(self.clear)
                                print("Account settings")
                                print("\n1. Set profile picture")
                                print("2. Set background image")
                                print("3. Update profile")
                                print("\n4. Go back")
                                wybor8 = input(f"\n{self.theme}Choice{Style.RESET_ALL}: ")

                                # ACCOUNT SETTINGS / SET PROFILE PIC
                                if wybor8 == "1":
                                    os.system(self.clear)
                                    print("Set profile picture")
                                    p_img = input("\nPlease input a name of your file: ")
                                    if p_img == "":
                                        continue
                                    else:
                                        self.t_bot.update_pfp(p_img)

                                elif wybor8 == "2":
                                    # ACCOUNT SETTINGS / SET BACKGROUND IMAGE
                                    os.system(self.clear)
                                    print("Set background image")
                                    b_img = input("\nPlease input a name of your file: ")
                                    if b_img == "":
                                        continue
                                    else:
                                        self.t_bot.update_bg(b_img)

                                elif wybor8 == "3":
                                    # ACCOUNT SETTINGS / UPDATE PROFILE
                                    os.system(self.clear)
                                    print("Update profile")
                                    print("\n1. Name")
                                    print("2. Location")
                                    print("3. Description")
                                    wybor9 = input(f"\n{self.theme}Choice{Style.RESET_ALL}: ")

                                    # UPDATE PROFILE / NAME
                                    if wybor9 == "1":
                                        os.system(self.clear)
                                        print("Change name")
                                        new_name = input("\nInput your new profile name: ")
                                        if new_name == "":
                                            continue
                                        print(f"\nYour profile name will be changed to {new_name}!")
                                        accept = input(f"Do you wish to accept it? ({self.theme}Y{Style.RESET_ALL}/n): ")

                                        if accept == "N" or accept == "n":
                                            pass

                                        else:
                                            self.t_bot.update_name(new_name)

                                    # UPDATE PROFILE / LOCATION
                                    elif wybor9 == "2":
                                        os.system(self.clear)
                                        print("Change location")
                                        new_loc = input("\nInput your new location: ")
                                        if new_loc == "":
                                            continue
                                        print(f"\nYour location will be changed to {new_loc}!")
                                        accept2 = input(f"Do you wish to accept it? ({self.theme}Y{Style.RESET_ALL}/n)")

                                        if accept2 == "N" or accept2 == "n":
                                            pass

                                        else:
                                            self.t_bot.update_location(new_loc)

                                    # UPDATE PROFILE / DESCRIPTION
                                    elif wybor9 == "3":
                                        os.system(self.clear)
                                        print("Change description")
                                        new_desc = input("\nInput your new description: ")
                                        if new_desc == "":
                                            continue
                                        accept3 = input(f"\nDo you wish to accept it? ({self.theme}Y{Style.RESET_ALL}/n)")

                                        if accept3 == "N" or accept3 == "n":
                                            pass

                                        else:
                                            self.t_bot.update_desc(new_desc)

                                # GO BACK TO OPTIONS
                                elif wybor8 == "4":
                                    break

                    # MAIN MENU THEME
                    elif wybor2 == "8":
                        os.system(self.clear)
                        print("Main menu theme")
                        print(f"\n1. Cyan {Fore.CYAN}//////{Style.RESET_ALL}")
                        print(f"2. Blue {Fore.BLUE}//////{Style.RESET_ALL}")
                        print(f"3. Magenta {Fore.MAGENTA}//////{Style.RESET_ALL}")
                        print(f"4. White {Fore.WHITE}//////{Style.RESET_ALL}")
                        print(f"\n{Fore.YELLOW}(Theme doesn\'t cover the entire program!){Style.RESET_ALL}")

                        t_input = input(f"Choose your desired {self.theme}theme{Style.RESET_ALL}: ")

                        # THEME CYAN
                        if t_input == "1":
                            self.theme = self.themetab[0]

                            self.set_config("Theme", "current", "0")

                            print(f"Theme has been set to {self.theme}CYAN{Style.RESET_ALL}")
                            time.sleep(1)

                        # THEME BLUE
                        elif t_input == "2":
                            self.theme = self.themetab[1]

                            self.set_config("Theme", "current", "1")

                            print(f"Theme has been set to {self.theme}BLUE{Style.RESET_ALL}")
                            time.sleep(1)

                        # THEME MAGENTA
                        elif t_input == "3":
                            self.theme = self.themetab[2]

                            self.set_config("Theme", "current", "2")

                            print(f"Theme has been set to {self.theme}MAGENTA{Style.RESET_ALL}")
                            time.sleep(1)

                        # THEME WHITE
                        elif t_input == "4":
                            self.theme = self.themetab[3]

                            self.set_config("Theme", "current", "3")

                            print(f"Theme has been set to {self.theme}WHITE{Style.RESET_ALL}")
                            time.sleep(1)

                    # GO BACK TO OPTIONS
                    elif wybor2 == "9":
                        break

            # EXIT PROGRAM
            elif wybor == "3":
                sys.exit()


if __name__ == "__main__":
    app = Main()
    try:
        app.mainloop()
    except Exception:
        if app.AUTHORIZED and app.send_errors:
            email_err()
            print(f"\n{Fore.RED}Error has occured, data has been sent to the creator!{Style.RESET_ALL}")
        else:
            print(f"\n{Fore.RED}Error has occured!{Style.RESET_ALL}")

        input(f"\nPress {Fore.RED}ENTER{Style.RESET_ALL} to exit...")
        sys.exit()
