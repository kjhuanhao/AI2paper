# -*- coding:utf-8 -*-
# @FileName  : SummaryChain.py
# @Time      : 2023/11/8
# @Author    : LaiJiahao
# @Desc      : 总结执行链

from models.LLM.SparkAI import SparkAI
from prompt.CommonPrompt import summary_prompt
from utils.PromptParser import PromptParser


class SummaryChain:
    """
    总结执行链
    """

    @staticmethod
    def run(prompt: str = None, *args):
        if args and prompt is None:
            content = args[0]
            prompt = PromptParser(summary_prompt, content=content)
        s = SparkAI()
        s.get_spark_result(prompt)
