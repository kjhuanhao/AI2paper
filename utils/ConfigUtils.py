# -*- coding:utf-8 -*-
# @FileName  : ConfigUtils.py
# @Time      : 2023/11/7
# @Author    : LaiJiahao
# @Desc      : 配置管理器

import json
from typing import Any


class ConfigUtils:
    """
    配置类
    """
    _config_path = "config/config.json"
    with open(_config_path) as f:
        config = json.load(f)

    def get_config(self, section: str, key: str) -> Any:
        """
        获取配置项
        :param section: 部分
        :param key: 键
        :return:
        """
        return self.config.get(section).get(key)


c = ConfigUtils()


class ErnieAIConfig:

    @staticmethod
    def get_client_id() -> str:
        return c.get_config("Ernie", "client_id")

    @staticmethod
    def get_client_secret() -> str:
        return c.get_config("Ernie", "client_secret")

    @staticmethod
    def get_access_token() -> str:
        return c.get_config("Ernie", "access_token")


class ZhipuAIConfig:

    @staticmethod
    def get_api_key() -> str:
        return c.get_config("Zhipu", "api_key")


class SparkAIConfig:

    @staticmethod
    def get_app_id() -> str:
        return c.get_config("Spark", "app_id")

    @staticmethod
    def get_api_secret() -> str:
        return c.get_config("Spark", "api_secret")

    @staticmethod
    def get_api_key() -> str:
        return c.get_config("Spark", "api_key")


class MinIOConfig:

    @staticmethod
    def get_access_key() -> str:
        return c.get_config("MinIo", "access_key")

    @staticmethod
    def get_secret_key() -> str:
        return c.get_config("MinIo", "secret_key")

    @staticmethod
    def get_host() -> str:
        return c.get_config("MinIo", "host")

    @staticmethod
    def get_port() -> int:
        return c.get_config("MinIo", "port")

    @staticmethod
    def get_bucket() -> str:
        return c.get_config("MinIo", "bucket")

    @staticmethod
    def get_tmp_path() -> str:
        return c.get_config("MinIo", "tmp_path")


class OpenAIConfig:
    @staticmethod
    def get_api_key() -> str:
        return c.get_config("OpenAI", "api_key")