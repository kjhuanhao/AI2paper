# -*- coding:utf-8 -*-
# @FileName  : JsonParser.py
# @Time      : 2023/11/7
# @Author    : LaiJiahao
# @Desc      : Json解析器


from typing import Dict
from loguru import logger


def Outline2json(outline: str) -> Dict[str, str]:
    """
    将outline转换为json格式
    :param outline 大纲
    :return: 返回json格式的大纲
    """
    logger.info("开始将大纲转换为json格式")
    outline = outline.replace("'''", "").replace("```", "")
    # 初始化一个空字典来存储结构化数据
    structured_data = {}

    # 将文本按行分割，并按照结构化格式存储
    lines = outline.split('\n')
    if len(lines) < 2:
        lines = outline.split('\\n')

    for line in lines:
        if line.strip():
            line = line.replace('"', "")
            structured_data[line] = ""

    filter_data = {k: v for k, v in structured_data.items() if k.strip()}

    logger.info("大纲Json数据转换成功!")
    return filter_data
