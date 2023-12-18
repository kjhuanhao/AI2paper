# -*- coding:utf-8 -*-
# @FileName  : OpenAI.py
# @Time      : 2023/12/1
# @Author    : LaiJiahao
# @Desc      : OpenAI

import openai

from entity.Response import Response
from utils.ConfigUtils import OpenAIConfig
from loguru import logger


class OpenAI:
    """
    OpenAI GPT-3 模型
    Example:
        oa = OpenAIGPT3()
        oa.get_openai_result(prompt)
    """
    openai.api_key = OpenAIConfig.get_api_key()
    _model = "text-davinci-003"

    def get_openai_result(self, prompt: str) -> Response:
        try:
            logger.info("OpenAI is working")
            response = openai.Completion.create(
                model=self._model,
                prompt=prompt,
                max_tokens=4000  # 可以根据需要调整生成的最大标记数
            )
            result_text = response.choices[0].text.strip() if response.choices else None
            tokens = response.usage.total_tokens if response.usage else None
            response = Response(result_text, tokens)
            logger.info("OpenAI 响应结果获取成功")
            return response
        except Exception as e:
            logger.error("OpenAI 响应结果获取失败: " + e.__str__())
