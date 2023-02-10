import pickle
from security_functions.cryptography import encrypt, decrypt
from aioredis.exceptions import RedisError
from socketio import AsyncRedisManager


class SioRedisManager(AsyncRedisManager):
    async def _publish(self, data):
        retry = True
        while True:
            try:
                if not retry:
                    self._redis_connect()
                return await self.redis.publish(
                    self.channel, encrypt(pickle.dumps(data)))
            except RedisError:
                if retry:
                    self._get_logger().error("Cannot publish to redis... "
                                             "retrying")
                    retry = False
                else:
                    self._get_logger().error("Cannot publish to redis... "
                                             "giving up")
                    break


    async def _listen(self):
        async for data in super()._listen():
            yield decrypt(data)
