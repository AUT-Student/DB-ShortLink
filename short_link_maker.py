import redis
import random
import string
import datetime


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
            print("before link")
            return self._previous_link(url)
        else:
            print("new link")
            return self._new_link(url)

    def reference_link(self, link):

        data = self.redis.hgetall("link:" + link)
        url = data["url"]
        reference_counter = data["reference_counter"]

        self.redis.hset(f"link:{link}", "reference_counter", int(reference_counter)+1)
        self.redis.hset(f"link:{link}", "last_reference", self._now_datetime_string())

        print(data)

        # print(datetime.datetime.strptime(data["last_reference"], "%d-%m-%y %H:%M:%S"))

    @staticmethod
    def random_string(letter_count=4, digit_count=2):
        """
        SOURCE: https://www.javatpoint.com/python-program-to-generate-a-random-string

        :param letter_count:
        :param digit_count:
        :return:
        """
        str1 = ''.join((random.choice(string.ascii_letters) for x in range(letter_count)))
        str1 += ''.join((random.choice(string.digits) for x in range(digit_count)))

        sam_list = list(str1)  # it converts the string to list.
        random.shuffle(sam_list)  # It uses a random.shuffle() function to shuffle the string.
        final_string = ''.join(sam_list)
        return final_string
