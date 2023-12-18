# -*- coding:utf-8 -*-
# @FileName  : Response.py
# @Time      : 2023/11/7
# @Author    : LaiJiahao
# @Desc      : None

import json


class Response:
    """
    响应类，用于封装大模型返回的结果
    """
    def __init__(self, result: str, tokens: int):
        self.result = result
        self.tokens = tokens

    def __str__(self):
        return json.dumps({
            "result": self.result,
            "tokens": self.tokens
        }, ensure_ascii=False)

    def __repr__(self):
        return self.__str__()

    def __eq__(self, other):
        return self.__dict__ == other.__dict__
