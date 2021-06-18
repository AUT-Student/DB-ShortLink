import redis
import random
import string


class ShortLinkMaker:
    def __init__(self):
        self._create_database_connection()
        # redis.set('foo', 'bar')
        # print(redis.get('foo'))

    def _create_database_connection(self):
        self.redis = redis.Redis(host='localhost', port=6379, db=0)

    def new_link(self, url):
        pass

    def reference_link(self, link):
        pass

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
