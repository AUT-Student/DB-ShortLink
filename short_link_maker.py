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
