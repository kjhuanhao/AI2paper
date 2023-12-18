# -*- coding:utf-8 -*-
# @FileName  : ExceptionHandler.py
# @Time      : 2023/11/10
# @Author    : LaiJiahao
# @Desc      : None

from loguru import logger


def retry_on_exception(max_retries=2):
    def decorator(func):
        def wrapper(*args, **kwargs):
            attempts = 0
            while attempts < max_retries + 1:
                try:
                    result = func(*args, **kwargs)
                    return result
                except Exception as e:
                    attempts += 1
                    logger.warning(f"Function {func.__name__} failed. Retrying... (Attempt {attempts}/{max_retries + 1})")
                    if attempts > max_retries:
                        logger.error("重试失败")
                        raise e

        return wrapper

    return decorator
