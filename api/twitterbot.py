from colorama import init, Fore, Style
from random import randint
import tweepy
import time
import os

# COLORAMA
init(convert=True)


class Twitterbot:

    def __init__(self, Auth1, Auth2, Auth3, Auth4):

        self.Auth1 = Auth1
        self.Auth2 = Auth2
        self.Auth3 = Auth3
        self.Auth4 = Auth4

        auth = tweepy.OAuthHandler(self.Auth1, self.Auth2)
        auth.set_access_token(self.Auth3, self.Auth4)
        self.api = tweepy.API(
            auth_handler=auth,
            wait_on_rate_limit=True,
            wait_on_rate_limit_notify=True
        )
        self.get_access()
        # DEFINE TWO LISTS FOR LATER USE
        # returned_list IS A LIST OF PEOPLE YOU FOLLOW
        # returned_list2 IS A LIST OF PEOPLE THAT FOLLOW YOU
        self.returned_list = self.check_who_you_follow()
        self.returned_list2 = self.check_who_follows_you()

    def __str__(self):

        print(f"\n{Fore.CYAN}Twitterbot{Style.RESET_ALL}:")
        print(f"Logged in as {Fore.CYAN}{self.myself.screen_name}{Style.RESET_ALL}")
        print("Validation codes:")
        print(f"Api key = {Fore.CYAN}{self.Auth1}{Style.RESET_ALL}")
        print(f"Api key secret = {Fore.CYAN}{self.Auth2}{Style.RESET_ALL}")
        print(f"Access token = {Fore.CYAN}{self.Auth3}{Style.RESET_ALL}")
        print(f"Access token secret = {Fore.CYAN}{self.Auth4}{Style.RESET_ALL}")
        return ""

    def get_access(self):
        # GET ACCESS IS HANDLED AUTOMATICALLY BY __init__() METHOD!

        print("Trying to connect to your Twitter account")
        # CHECKS FOR CONNECTION
        try:
            self.myself = self.api.me()

        except tweepy.TweepError as err:
            print(f"{Fore.RED}{err.reason}{Style.RESET_ALL}")
            input(f"\nPress {Fore.CYAN}ENTER{Style.RESET_ALL} to continue...")

        else:
            print(f"{Fore.GREEN}Connection established!{Style.RESET_ALL}")
            print(f"Hello {Fore.CYAN}{self.myself.screen_name}{Style.RESET_ALL}!")

    # USED IN follow_random()
    @staticmethod
    def randomizer(number):

        return randint(0, number)

    @staticmethod
    def searchForFile(p):

        suppExtensions = ["jpg", "jpeg", "png", "gif"]

        dirList = os.listdir()
        for ext in suppExtensions:
            pWithExt = f"{p}.{ext}"
            if os.path.exists(pWithExt):
                fileLocation = f"{os.getcwd()}\\{pWithExt}"
                os.chdir("..")
                return fileLocation
            else:
                for dir in dirList:
                    if os.path.isdir(dir):
                        os.chdir(dir)
                        if os.path.exists(pWithExt):
                            fileLocation = f"{os.getcwd()}\\{pWithExt}"
                            os.chdir("..")
                            return fileLocation
                        else:
                            pass

                        os.chdir("..")
                    else:
                        pass

        return False

    def update_pfp(self, pic):

        filePath = Twitterbot.searchForFile(pic)

        if not filePath:
            print(f"\n{Fore.YELLOW}File doesn\'t exist...{Style.RESET_ALL}")
            time.sleep(1)
            return

        try:
            self.api.update_profile_image(filename=filePath)

        except tweepy.TweepError as err:
            print(f"{Fore.RED}{err.reason}{Style.RESET_ALL}")
            time.sleep(1)

        else:
            print(f"{Fore.GREEN}Profile picture updated!{Style.RESET_ALL}")
            time.sleep(1)

    def update_bg(self, pic):

        filePath = Twitterbot.searchForFile(pic)

        if not filePath:
            print(f"\n{Fore.YELLOW}File doesn\'t exist...{Style.RESET_ALL}")
            time.sleep(1)
            return

        try:
            self.api.update_profile_background_image(filename=filePath)

        except tweepy.TweepError as err:
            print(f"{Fore.RED}{err.reason}{Style.RESET_ALL}")
            time.sleep(1)

        else:
            print(f"{Fore.GREEN}Background image updated!{Style.RESET_ALL}")
            time.sleep(1)

    def update_name(self, prof_name):

        try:
            self.api.update_profile(name=prof_name)

        except tweepy.TweepError as err:
            print(f"{Fore.RED}{err.reason}{Style.RESET_ALL}")
            time.sleep(1)

        else:
            print(f"{Fore.GREEN}Name set to {prof_name}!{Style.RESET_ALL}")
            time.sleep(1)

    def update_location(self, prof_loc):

        try:
            self.api.update_profile(location=prof_loc)

        except tweepy.TweepError as err:
            print(f"{Fore.RED}{err.reason}{Style.RESET_ALL}")
            time.sleep(1)

        else:
            print(f"{Fore.GREEN}Location set to {prof_loc}!{Style.RESET_ALL}")
            time.sleep(1)

    def update_desc(self, prof_desc):

        try:
            self.api.update_profile(description=prof_desc)

        except tweepy.TweepError as err:
            print(f"{Fore.RED}{err.reason}{Style.RESET_ALL}")
            time.sleep(1)

        else:
            print(f"{Fore.GREEN}Desctiption set!{Style.RESET_ALL}")
            time.sleep(1)

    def post_tweet(self, messImg, media, i):

        if not media:
            while True:
                if i == 0:
                    choice = input(f"\nDo you wish to send an image alongside the text? (y/{Fore.CYAN}N{Style.RESET_ALL}): ")

                    if choice == "":
                        choice = "N"

                else:
                    choice = "N"

                if choice == "n" or choice == "N":
                    try:
                        self.api.update_status(status=messImg)

                    except tweepy.TweepError as err:
                        print(f"{Fore.RED}{err.reason}{Style.RESET_ALL}")
                        return False

                    else:
                        print(f"{Fore.GREEN}\nTweet sent!{Style.RESET_ALL}\n")
                        return True

                elif choice == "y" or choice == "Y":
                    file = input(f"Please enter the name of your file: ")

                    filePath = Twitterbot.searchForFile(file)

                    if not filePath:
                        print(f"\n{Fore.YELLOW}File doesn\'t exist...{Style.RESET_ALL}")

                        try:
                            self.api.update_status(status=messImg)

                        except tweepy.TweepError as err:
                            print(f"{Fore.RED}{err.reason}{Style.RESET_ALL}")
                            return False

                        else:
                            print(f"{Fore.GREEN}\nTweet sent without image!{Style.RESET_ALL}\n")
                            return True

                    else:
                        try:
                            self.api.update_with_media(filename=filePath, status=messImg)

                        except tweepy.TweepError as err:
                            print(f"{Fore.RED}{err.reason}{Style.RESET_ALL}")
                            return False

                        else:
                            print(f"{Fore.GREEN}\nTweet sent with image!{Style.RESET_ALL}\n")
                            return True

                else:
                    print(f"{Fore.RED}Not a valid choice!{Style.RESET_ALL}")
                    continue

        elif media:
            while True:
                if i == 0:
                    choice = input(f"\nDo you wish to send a text alongside the image? (y/{Fore.CYAN}N{Style.RESET_ALL}): ")

                    if choice == "":
                        choice = "N"

                else:
                    choice = "N"

                if choice == "n" or choice == "N":

                    try:
                        file = open(messImg, "rb")
                        media = self.api.media_upload(filename=messImg, file=file)
                        m_ids = [media.media_id_string]
                        self.api.update_status(media_ids=m_ids)
                        file.close()

                    except tweepy.TweepError as err:
                        print(f"{Fore.RED}{err.reason}{Style.RESET_ALL}")
                        return False

                    else:
                        print(f"{Fore.GREEN}\nTweet sent!{Style.RESET_ALL}\n")
                        return True

                elif choice == "y" or choice == "Y":
                    text = input(f"Please insert your text ({Fore.CYAN}Hashtags{Style.RESET_ALL} etc.): ")

                    try:
                        file = open(messImg, "rb")
                        media = self.api.media_upload(filename=messImg, file=file)
                        file.close()
                        m_ids = [media.media_id_string]
                        self.api.update_status(
                            status=text,
                            media_ids=m_ids
                        )

                    except tweepy.TweepError as err:
                        print(f"{Fore.RED}{err.reason}{Style.RESET_ALL}")
                        return False

                    else:
                        print(f"{Fore.GREEN}\nTweet sent!{Style.RESET_ALL}\n")
                        return True

                else:
                    print(f"{Fore.RED}Not a valid choice!{Style.RESET_ALL}")
                    continue

    def check_timeline(self, p_tweets):

        post_dict = {}

        print(f"\nYou follow {Fore.CYAN}{str(len(self.returned_list))}{Style.RESET_ALL} user/s!")
        print(f"{Fore.CYAN}{str(len(self.returned_list2))}{Style.RESET_ALL} user/s follow you!")

        print(f"\nYour last {Fore.CYAN}{p_tweets}{Style.RESET_ALL} tweets:")

        for index, post in enumerate(self.api.user_timeline(count=p_tweets)):

            post_dict.update({index: post._json["text"]})
            if index == (int(p_tweets) - 1):
                post_dict.update({"username": post._json["user"]["screen_name"]})

        return post_dict

    @staticmethod
    def make_decision(text):

        blacklisted = [
            "covid", "covid-19", "coronavirus", "sad", "terrible",
            "racist", "racism", "cancer", "disease", "pandemic",
            "death", "dead", "accident", "horrible", "rip",
            "r.i.p", "trump", "president", "bad", "terrifying",
            "murder", "homicide", "shooting", "blm", "blacklivesmatter",
            "war", "kill", "killing", "bullying", "harassment",
            "harassing", "harassed", "disturbing", "disturbed", "horrifying",
            "horrified", "abuse"
        ]

        good = [
            "happy", "fantastic", "good", "perfect", "love",
            "happiness", "joy", "great", "cool", "amazing",
            "incredible", "fun", "funny", "gift", "motivation",
            "cheer", "success", "successful", "smile", "beautiful",
            "awesome"
        ]

        # Removes http
        just_text = text.split("http")
        bad_cnt = 0
        good_cnt = 0

        for bad_word in blacklisted:

            args = [bad_word, bad_word.upper(), bad_word.capitalize()]

            for arg in args:
                if arg in just_text[0]:
                    bad_cnt += 1

        for good_word in good:

            args = [good_word, good_word.upper(), good_word.capitalize()]

            for arg in args:
                if arg in just_text[0]:
                    good_cnt += 1

        # If there are 2 times more good words than bad words or there are no bad words then True
        if bad_cnt == 0 or good_cnt > (bad_cnt * 2):
            return True
        else:
            return False

    def tweet_like(self, hmany, relate, w_time, reply):

        # THANKS TO THIS THE TEXT DOESN'T OVERLAP
        time.sleep(0.3)

        msgs = [
            f"That\'s pretty cool, follow me for more {relate}",
            f"Fantastic! I have some more {relate}, so you can follow me if you want :)",
            f"That\'s great! I have {relate} too!",
            f"Wow, that\'s amazing!",
            f"Incredible, love that! If you seek {relate} you can follow me for some btw",
            f"That\'s Pretty neat!"
        ]

        print(f"3. {Fore.CYAN}Looking for tweets to like{Style.RESET_ALL}")

        for tweet in tweepy.Cursor(
            self.api.search, q=relate,
            tweet_mode="extended", lang="en"
        ).items(hmany):

            try:
                author_id = tweet.author._json["id"]
                twt_id = tweet._json["id"]
                try:
                    twt_txt = tweet.retweeted_status.full_text
                except AttributeError:
                    twt_txt = tweet.full_text
                if author_id != self.myself.id:
                    tweet.favorite()
                    try:
                        decision = Twitterbot.make_decision(twt_txt)

                        if decision and reply:
                            self.api.update_status(
                                status=msgs[Twitterbot.randomizer(5)],
                                in_reply_to_status_id=twt_id,
                                auto_populate_reply_metadata=True
                            )
                    except tweepy.TweepError:
                        pass
                else:
                    pass

            except tweepy.TweepError as err:
                code = err.response.status_code

                if code == 403:
                    continue

                else:
                    print(f"3. {Fore.YELLOW}{err.reason}{Style.RESET_ALL}")
                    return

            else:
                time.sleep(int(w_time))

        print(f"3. {Fore.GREEN}Done liking tweets!{Style.RESET_ALL}")

    def check_if_dm_already_sent(self):

        already_dmd = []
        dms = self.api.list_direct_messages()

        for dm in dms:

            rec_id = dm.message_create["target"]["recipient_id"]

            if rec_id in already_dmd:
                continue

            else:
                already_dmd.append(rec_id)

        return already_dmd

    def check_who_follows_you(self):

        they_do = []

        for follower_id in tweepy.Cursor(self.api.followers_ids).items():

            they_do.append(follower_id)

        return they_do

    def check_who_you_follow(self):

        already_followed = []

        for friend_id in tweepy.Cursor(self.api.friends_ids).items():

            already_followed.append(friend_id)

        return already_followed

    def follow_back(self, w_time):

        time.sleep(0.1)

        print(f"1. {Fore.CYAN}Trying to follow back all your followers{Style.RESET_ALL}")

        for follower in self.returned_list2:

            if follower in self.returned_list:
                continue

            else:
                try:
                    self.api.create_friendship(id=follower)
                    self.returned_list.append(follower)

                except tweepy.TweepError:
                    pass

                else:
                    time.sleep(int(w_time))

        print(f"1. {Fore.GREEN}I successfully followed all your followers!{Style.RESET_ALL}")

    def unfollow_v2(self, w_time):

        # THANKS TO THIS TEXT DOESN'T OVERLAP
        time.sleep(0.2)

        print(f"2. {Fore.CYAN}Searching for people to unfollow{Style.RESET_ALL}")

        for user_id in self.returned_list:

            if user_id in self.returned_list2:
                continue

            else:
                try:
                    self.api.destroy_friendship(id=user_id)
                    self.returned_list.remove(user_id)

                except tweepy.TweepError as err:
                    print(f"2. {Fore.YELLOW}{err.reason}{Style.RESET_ALL}")
                    return

                else:
                    time.sleep(int(w_time))

        print(f"2. {Fore.GREEN}Done unfollowing users!{Style.RESET_ALL}")

    def send_dm(self, per_id, per_sn, rel):

        val2 = Twitterbot.randomizer(7)
        msg = [
            f"Hello, if you like {rel}, follow my account!",
            f"I have a lot of {rel} on my account, come check it out!",
            f"I\'m interested in {rel}, if you\'re interested in {rel} too then feel free to follow me!",
            f"Hi, I\'d like to invite you to follow my account for some {rel}",
            f"Hello there! I really like your profile, please check out mine and leave a follow!",
            f"Hey, make sure to follow me back for some {rel}!",
            f"Hey, if you seek some awesome {rel} follow me!",
            f"Hello, I post {rel} daily follow me if you are in need of some!"
        ]

        try:
            self.api.send_direct_message(recipient_id=per_id, text=msg[val2])

        except tweepy.TweepError:
            return

    def follow_random(self, relate, ile_fo, w_time, reply):

        already_sent = self.check_if_dm_already_sent()
        value = Twitterbot.randomizer(50)

        print(f"4. {Fore.CYAN}Looking for {ile_fo} users to follow{Style.RESET_ALL}")

        # (QUERY, HOW MANY USERS FROM THAT PAGE, HOW MANY PAGES)
        users = self.api.search_users(q=relate, count=ile_fo, page=value)

        for person in users:

            if person.id in self.returned_list:
                continue

            else:
                try:
                    person.follow()
                    self.returned_list.append(person.id)
                    if person.id in already_sent:
                        pass
                    else:
                        if reply:
                            self.send_dm(person.id, person.screen_name, relate)

                except tweepy.TweepError:
                    pass

                else:
                    time.sleep(int(w_time))

        print(f"4. {Fore.GREEN}Done following new users!{Style.RESET_ALL}")
