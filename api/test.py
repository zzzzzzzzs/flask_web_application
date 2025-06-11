import asyncio
import time

from flask_restplus import Resource

from api import api
from flask import request
from aiohttp import ClientSession
from aiohttp.client import ClientTimeout
import requests
ns = api.namespace('test', description='User operations')


async def fetch(url, headers, params=None, timeout=30):
    async with ClientSession(headers=headers, timeout=ClientTimeout(total=timeout)) as session:
        async with session.get(url, params=params, ssl=False) as response:
            try:
                ret = await response.json()
            except:
                ret = await response.text()

            return response, ret

def sync_fetch(url, headers):
    requests.get(url, headers=headers)


@ns.route('/async')
class AsyncTest(Resource):

    def get(self):
        urls = [
            'http://localhost:8000/test/5',
            'http://localhost:8000/test/10',
            'http://localhost:8000/test/20',
        ]
        st = time.time()
        tasks = [fetch(url, headers=request.headers) for url in urls]
        try:
            loop = asyncio.get_event_loop()
        except:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
        res_list = loop.run_until_complete(asyncio.gather(*tasks))

        # for resp, ret in res_list:
        #     print(resp)
        #     print(ret)

        time_cost = time.time() - st
        return {"async_time_cost": time_cost}


@ns.route('/sync')
class SyncTest(Resource):
    def get(self):
        urls = [
            'http://localhost:8000/test/5',
            'http://localhost:8000/test/10',
            'http://localhost:8000/test/20',
        ]
        st = time.time()
        for url in urls:
            sync_fetch(url, request.headers)

        time_cost = time.time() - st
        return {"sync_time_cost": time_cost}