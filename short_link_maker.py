import redis
import random
import string
import datetime
import webbrowser
import prettytable
import matplotlib.pyplot as plt


class ShortLinkMaker:
    def __init__(self):
        self._create_database_connection()
        self.expiration_time = 7 * 24 * 60 * 60

    def _create_database_connection(self):
        self.redis = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)

    @staticmethod
    def _now_datetime_string():
        return datetime.datetime.now().strftime("%d-%m-%y %H:%M:%S")

    def _new_link(self, url):
        link = self.random_string()
        new_data = {"url": url, "reference_counter": 0,
                    "last_reference": self._now_datetime_string()}
        self.redis.hmset(f"link:{link}", new_data)
        self.redis.expire(f"link:{link}", self.expiration_time)
        self.redis.set(f"url:{url}", link, ex=self.expiration_time)

        return link

    def _previous_link(self, url):
        return self.redis.get(f"url:{url}")

    def _is_exist(self, key):
        return self.redis.exists(key) == 1

    def _increase_daily_submit(self):
        date_string = datetime.datetime.now().strftime("%d%m%y")
        key = f"daily_submit:{date_string}"

        if self._is_exist(key):
            self.redis.set(key, int(self.redis.get(key)) + 1)
        else:
            self.redis.set(key, 1)

    def _increase_daily_reference(self):
        date_string = datetime.datetime.now().strftime("%d%m%y")
        key = f"daily_reference:{date_string}"

        if self._is_exist(key):
            self.redis.set(key, int(self.redis.get(key)) + 1)
        else:
            self.redis.set(key, 1)

    def reset(self):
        for key in self.redis.scan_iter("*"):
            self.redis.delete(key)

    def debug(self):

        print("\nDebug:")

        table = prettytable.PrettyTable()
        table.field_names = ["key", "value"]
        for key in self.redis.scan_iter("link:*"):
            table.add_row([key, self.redis.hgetall(key)])
        print(table)

        table = prettytable.PrettyTable()
        table.field_names = ["key", "value"]
        for key in self.redis.scan_iter("url:*"):
            table.add_row([key, self.redis.get(key)])
        print(table)

        table = prettytable.PrettyTable()
        table.field_names = ["key", "value"]
        for key in self.redis.scan_iter("daily*"):
            table.add_row([key, self.redis.get(key)])
        print(table)

    def submit_url(self, url):
        self._increase_daily_submit()
        exist_before = self._is_exist(f"url:{url}")
        if exist_before:
            return self._previous_link(url)
        else:
            return self._new_link(url)

    def reference_link(self, link):
        self._increase_daily_reference()
        exist_url = self._is_exist(f"link:{link}")
        if exist_url:

            data = self.redis.hgetall("link:" + link)
            url = data["url"]
            reference_counter = data["reference_counter"]

            self.redis.hset(f"link:{link}", "reference_counter", int(reference_counter)+1)
            self.redis.hset(f"link:{link}", "last_reference", self._now_datetime_string())

            self.redis.expire(f"link:{link}", self.expiration_time)
            self.redis.expire(f"url:{url}", self.expiration_time)

            self.open_url_on_browser(url)
            return url
        else:
            return "ERROR"

    def dashboard(self):
        link_list = []
        for key in self.redis.scan_iter("link:*"):
            value = self.redis.hgetall(key)
            item_datetime = datetime.datetime.strptime(value["last_reference"], "%d-%m-%y %H:%M:%S")
            difference = datetime.datetime.now() - item_datetime
            remaining = self.expiration_time - difference.total_seconds()

            dictionary = {"key": key[5:], "url": value["url"],
                          "reference_counter": int(value["reference_counter"]),
                          "last_reference": value["last_reference"], "remaining": remaining}

            link_list.append(dictionary)

        print("\nAll Links:")
        table = prettytable.PrettyTable()

        table.field_names = ["Row", "Key", "URL", "Reference Counter", "Last Reference", "Remaining Expiration Time"]
        for i, item in enumerate(link_list):
            table.add_row([i+1, item["key"], item["url"], item["reference_counter"],
                           item["last_reference"], item["remaining"]])

        print(table)
        sorted_link_list = sorted(link_list, key=lambda x: -x["reference_counter"])

        print("\nMore Frequent Link:")
        table = prettytable.PrettyTable()
        table.field_names = ["Rank", "Key", "URL", "Reference Counter", "Last Reference", "Remaining Expiration Time"]
        for rank, item in enumerate(sorted_link_list):
            table.add_row([rank+1, item["key"], item["url"], item["reference_counter"],
                           item["last_reference"], item["remaining"]])
            if rank == 2:
                break
        print(table)
        data = []
        for key in self.redis.scan_iter("daily_submit:*"):
            value = int(self.redis.get(key))
            data.append({"day": key[13:], "counter": value})

        data = sorted(data, key=lambda x: x["day"])
        days = []
        counters = []
        for item in data:
            days.append(item["day"])
            counters.append(item["counter"])

        plt.title("Daily Submit Statistic")
        plt.bar(days, counters)
        plt.show()

        days = []
        counters = []
        for key in self.redis.scan_iter("daily_reference:*"):
            value = int(self.redis.get(key))
            days.append(key[16:])
            counters.append(value)

        plt.title("Daily Reference Statistic")
        plt.bar(days, counters)
        plt.show()

    @staticmethod
    def open_url_on_browser(url):
        ie = webbrowser.get('c:\\program files\\internet explorer\\iexplore.exe')
        ie.open(url)

    @staticmethod
    def random_string(letter_count=4, digit_count=2):
        """
        SOURCE: https://www.javatpoint.com/python-program-to-generate-a-random-string

        :param letter_count: number of letter chars
        :param digit_count: number of digit chars
        :return: random string
        """
        str1 = ''.join((random.choice(string.ascii_letters) for x in range(letter_count)))
        str1 += ''.join((random.choice(string.digits) for x in range(digit_count)))

        sam_list = list(str1)  # it converts the string to list.
        random.shuffle(sam_list)  # It uses a random.shuffle() function to shuffle the string.
        final_string = ''.join(sam_list)
        return final_string
