import time
from channels.generic.http import AsyncHttpConsumer
from asgiref.sync import sync_to_async


async_sleep = sync_to_async(time.sleep)


class BasicHttpConsumer(AsyncHttpConsumer):
    async def handle(self, body):
        await async_sleep(10)

        await self.send_response(200, b"Your response bytes", headers=[
            ("Content-Type", "text/plain"),
        ])

