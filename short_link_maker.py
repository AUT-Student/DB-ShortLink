import redis
import random
import string
import datetime
import webbrowser


class ShortLinkMaker:
    def __init__(self):
        self._create_database_connection()

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
        self.redis.set(f"url:{url}", link)

        return link

    def _previous_link(self, url):
        return self.redis.get(f"url:{url}")

    def _is_exist(self, key):
        return self.redis.exists(key) == 1

    def _increase_daily_submit(self):
        date_string = datetime.datetime.now().strftime("%d-%m-%y")
        key = f"daily_submit:{date_string}"

        if self._is_exist(key):
            self.redis.set(key, self.redis.get(key) + 1)
        else:
            self.redis.set(key, 1)

    def _increase_daily_statistics_reference(self):
        pass

    def reset(self):
        for key in self.redis.scan_iter("*"):
            self.redis.delete(key)

    def debug(self):
        for key in self.redis.scan_iter("*"):
            print(key)
            print(self.redis.get(key))

    def submit_url(self, url):
        exist_before = self._is_exist(f"url:{url}")
        if exist_before:
            return self._previous_link(url)
        else:
            return self._new_link(url)

    def reference_link(self, link):
        exist_url = self._is_exist(f"link:{link}")
        if exist_url:

            data = self.redis.hgetall("link:" + link)
            url = data["url"]
            reference_counter = data["reference_counter"]

            self.redis.hset(f"link:{link}", "reference_counter", int(reference_counter)+1)
            self.redis.hset(f"link:{link}", "last_reference", self._now_datetime_string())

            self.open_url_on_browser(url)
            return url
        else:
            return "ERROR"


        # print(datetime.datetime.strptime(data["last_reference"], "%d-%m-%y %H:%M:%S"))

    def dashboard(self):
        link_list = []
        for key in self.redis.scan_iter("link:*"):
            value = self.redis.hgetall(key)
            dictionary = {"key": key[4:], "url": value["url"],
                          "reference_counter": int(value["reference_counter"]),
                          "last_reference": value["last_reference"]}

            link_list.append(dictionary)

        print("All Links:")
        for item in link_list:
            print(item)

        print()
        sorted_link_list = sorted(link_list, key=lambda x: -x["reference_counter"])

        print("More Frequent Link:")
        print(sorted_link_list[0])
        print(sorted_link_list[1])
        print(sorted_link_list[2])
        print()

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
