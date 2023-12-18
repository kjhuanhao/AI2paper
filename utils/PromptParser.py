# -*- coding:utf-8 -*-
# @FileName  : PromptParser.py
# @Time      : 2023/11/7
# @Author    : LaiJiahao
# @Desc      : Prompt解析器

import re


def PromptParser(prompt, **kwargs) -> str:
    """
    prompt解析器，用于构建prompt模板
    :param prompt: 提示词模板
    :param kwargs: 提示词中的参数
    :return:
    """
    for key, value in kwargs.items():
        pattern = r'\{' + key + r'\}'
        prompt = re.sub(pattern, str(value), prompt)

    remaining_placeholders = re.findall(r'\{.*?\}', prompt)
    if remaining_placeholders:
        raise ValueError("缺少参数: " + ", ".join(remaining_placeholders))
    return prompt
