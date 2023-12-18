# -*- coding:utf-8 -*-
# @FileName  : SparkAI.py
# @Time      : 2023/11/8
# @Author    : LaiJiahao
# @Desc      : 星火AI大模型

import websockets
import json
import hmac
import hashlib
import base64
from time import mktime
from wsgiref.handlers import format_date_time
from urllib.parse import urlparse, urlencode
import asyncio
from utils.ConfigUtils import SparkAIConfig
from datetime import datetime
from loguru import logger
from entity.Response import Response


class SparkAI:
    """
    SparkAI大模型
    Example:
        s = SparkAI()
        s.get_spark_result(prompt)
    """
    def __init__(self):
        self._api_key = SparkAIConfig.get_api_key()
        self._api_secret = SparkAIConfig.get_api_secret()
        self._app_id = SparkAIConfig.get_app_id()
        self._url = "wss://spark-api.xf-yun.com/v3.1/chat"
        self.host = urlparse(self._url).netloc
        self.path = urlparse(self._url).path
        self._domain = "generalv3"

    def _create_url(self):
        now = datetime.now()
        date = format_date_time(mktime(now.timetuple()))
        signature_origin = "host: " + self.host + "\n"
        signature_origin += "date: " + date + "\n"
        signature_origin += "GET " + self.path + " HTTP/1.1"

        signature_sha = hmac.new(self._api_secret.encode('utf-8'), signature_origin.encode('utf-8'),
                                 digestmod=hashlib.sha256).digest()

        signature_sha_base64 = base64.b64encode(signature_sha).decode(encoding='utf-8')
        authorization_origin = f'api_key="{self._api_key}", algorithm="hmac-sha256", headers="host date request-line", signature="{signature_sha_base64}"'
        authorization = base64.b64encode(authorization_origin.encode('utf-8')).decode(encoding='utf-8')

        v = {
            "authorization": authorization,
            "date": date,
            "host": self.host
        }
        url = self._url + '?' + urlencode(v)
        return url

    def _gen_params(self, prompt):
        data = {
            "header": {
                "app_id": self._app_id,
                "uid": "1234"
            },
            "parameter": {
                "chat": {
                    "domain": self._domain,
                    "temperature": 0.5,
                    "max_tokens": 2048
                }
            },
            "payload": {
                "message": {
                    "text": [{"role": "user", "content": prompt}]
                }
            }
        }
        return data

    def get_spark_result(self, prompt):
        try:
            logger.info("SparkAI is working")
            ws = _WebSocketClient()
            response = asyncio.run(ws.start(self._create_url(), self._gen_params(prompt)))
            logger.info("星火大模型响应结果获取成功")
            return response
        except Exception as e:
            logger.error("星火大模型响应结果获取失败: " + e.__str__())


class _WebSocketClient:

    def __init__(self):
        self.result = ""

    @staticmethod
    async def send_data(websocket, data):
        await websocket.send(data)

    async def on_message(self, websocket, message):
        data = json.loads(message)
        code = data['header']['code']
        if code != 0:
            logger.info(f'请求错误: {code}, {data}')
            await websocket.close()
        else:
            choices = data["payload"]["choices"]
            status = choices["status"]
            content = choices["text"][0]["content"]
            self.result += content
            if status == 2:
                total_tokens = data["payload"]["usage"]["text"]["total_tokens"]
                await websocket.close()
                return total_tokens

    async def start(self, url, data) -> Response:
        total_tokens = None
        async with websockets.connect(url, ssl=True) as websocket:
            await self.send_data(websocket, json.dumps(data))
            async for message in websocket:
                total_tokens = await self.on_message(websocket, message)
                if total_tokens:
                    total_tokens = total_tokens
        return Response(self.result, total_tokens)
