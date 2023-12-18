# -*- coding:utf-8 -*-
# @FileName  : ErnieAI.py
# @Time      : 2023/11/7
# @Author    : LaiJiahao
# @Desc      : 文心一言大模型

import json
import requests

from entity.Response import Response
from loguru import logger
from utils.ConfigUtils import ErnieAIConfig


class ErnieBotAI:
    """
    文心一言大模型
    Example:
        e = ErnieBotAI()
        e.get_ernie_result(prompt)
    """
    _access_token_url = "https://aip.baidubce.com/oauth/2.0/token"
    _ernie_url = "https://aip.baidubce.com/rpc/2.0/ai_custom/v1/wenxinworkshop/chat/completions"

    def __init__(self):
        self._client_id = ErnieAIConfig.get_client_id()
        self._client_secret = ErnieAIConfig.get_client_secret()
        self._access_token = ErnieAIConfig.get_access_token()

    def get_ernie_result(self, prompt: str) -> Response | RuntimeError:
        """
        获取文心一言的结果
        :param prompt: 提示词
        :return:
        """
        headers = {
            'Content-Type': 'application/json'
        }
        payload = {
            "access_token": self._access_token
        }
        data = json.dumps({
            "messages": [
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        })
        logger.info("ErnieAI is working")
        response = requests.post(self._ernie_url, headers=headers, params=payload, data=data)
        response = response.json()
        try:
            response = Response(response["result"], response["usage"]["total_tokens"])
            logger.info("文心一言大模型响应结果获取成功")
            return response
        except Exception as e:
            logger.error("文心一言大模型响应结果获取失败: " + e.__str__())

    def get_access_token(self) -> str:
        """
        获取文心一言的access_token
        :return:
        """
        payload = {
            "grant_type": "client_credentials",
            "client_id": self._client_id,
            "client_secret": self._client_secret
        }
        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }

        response = requests.post(self._access_token_url, headers=headers, params=payload)
        return response.json().get("access_token")
