# -*- coding:utf-8 -*-
# @FileName  : ZhipuAI.py
# @Time      : 2023/11/7
# @Author    : LaiJiahao
# @Desc      : 智普清言

import zhipuai

from utils.ConfigUtils import ZhipuAIConfig
from entity.Response import Response
from loguru import logger


class ZhipuAI:
    """
    智普清言大模型
    Example:
        z = ZhipuAI()
        z.get_zhipu_result(prompt)
    """
    zhipuai.api_key = ZhipuAIConfig.get_api_key()
    _model = "chatglm_turbo"

    def get_zhipu_result(self, prompt: str) -> Response:
        logger.info("ZhipuAI is working")
        response = zhipuai.model_api.invoke(
            model=self._model,
            prompt=[
                {"role": "user", "content": prompt},
            ]
        )
        try:
            response = Response(response["data"]["choices"][0]["content"], response["data"]["usage"]["total_tokens"])
            logger.info("智普清言大模型响应结果获取成功")
            return response
        except Exception as e:
            logger.error("智普清言大模型响应结果获取失败: " + e.__str__())
