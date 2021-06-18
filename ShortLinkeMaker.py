import redis


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
