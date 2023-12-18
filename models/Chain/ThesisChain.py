# -*- coding:utf-8 -*-
# @FileName  : ThesisChain.py
# @Time      : 2023/11/8
# @Author    : LaiJiahao
# @Desc      : 论文生成执行链

import json
import concurrent.futures
import random
from prompt.ThesisPrompt import (
    thesis_outline_prompt,
    thesis_content_prompt,
    thesis_refinish_prompt
)
from utils.PromptParser import PromptParser
from models.LLM.ZhipuAI import ZhipuAI
from models.LLM.SparkAI import SparkAI
from models.LLM.ErnieAI import ErnieBotAI
from utils.JsonParser import Outline2json
from loguru import logger
from utils.ExceptionHandler import retry_on_exception
from threading import Lock


class ThesisChain:

    def __init__(self, uuid: str):
        self.short_term_memory = None
        self.total_tokens = 0
        self.outline_json = None
        self.outline = None
        self.s = SparkAI()
        self.z = ZhipuAI()
        # self.e = ErnieBotAI()
        self.lock = Lock()
        self.uuid = uuid

    def run(self, keyword: str):
        logger.info("论文开始生成")
        self._generate_outline(keyword)
        print(self.outline_json)
        logger.info("开始生成论文正文")
        outline_keys = self.outline_json.keys()
        total_process = len(outline_keys)
        current_process = 1

        with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
            futures = []

            def done_callback(futures):
                nonlocal current_process
                logger.info(f"当前进程: {current_process}/{total_process}")
                current_process += 1

            for key in outline_keys:
                title_list = [v for v in key.split(" ") if v]

                level = title_list[0]
                title = title_list[-1]

                if len(level.split(".")) == 1:
                    current_process += 1
                    continue

                content_prompt = PromptParser(thesis_content_prompt, keyword=keyword, title=title)
                future = executor.submit(self._generate_content, key, content_prompt)
                future.add_done_callback(done_callback)
                futures.append(future)

        with open(f"output/{self.uuid}.json", "a", encoding="utf-8") as f:
            f.write(json.dumps(self.outline_json))
        print(self.total_tokens)

    @retry_on_exception()
    def _generate_outline(self, keyword: str) -> None:
        outline_prompt = PromptParser(thesis_outline_prompt, keyword=keyword)
        outline = self.z.get_zhipu_result(outline_prompt).result
        outline_json = Outline2json(outline)
        with self.lock:
            new_outline_json = outline_json.copy()
            for key in outline_json:
                title_list = [v for v in key.split(" ") if v]
                if len(title_list) != 2:
                    new_outline_json.pop(key)
            self.outline_json = new_outline_json
        self.outline = outline
        logger.info("大纲生成完毕")

    @retry_on_exception()
    def _generate_content(self, key: str, content_prompt: str) -> str:
        random_func = random.choice([self.s.get_spark_result, self.z.get_zhipu_result])
        content_response = random_func(content_prompt)
        content_result = content_response.result
        self.outline_json[key] = content_result
        self.total_tokens += content_response.tokens
        print(content_result)
        return content_result

