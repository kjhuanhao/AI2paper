# -*- coding:utf-8 -*-
# @FileName  : MinIO.py
# @Time      : 2023/11/7
# @Author    : LaiJiahao
# @Desc      : 主运行程序

import fitz
import io

from minio import Minio
from utils.ConfigUtils import MinIOConfig
from minio.helpers import ObjectWriteResult
from typing import IO, Tuple
from docx import Document


class MinIOUtil:
    """
    MinIO 文件上传工具类
    Example:
        from utils.MinIO import MinIOUtil
    m = MinIOUtil()
    print(m.put_object("output.pdf", "output/output.pdf"))
    """
    def __init__(self):
        self.bucket_name = MinIOConfig.get_bucket()
        self.client = Minio(
            f"{MinIOConfig.get_host()}:{MinIOConfig.get_port()}",
            access_key=MinIOConfig.get_access_key(),
            secret_key=MinIOConfig.get_secret_key(),
            secure=False
        )

    def put_object(self, object_name: str, file_path: str, *args, **kwargs) -> Tuple:
        """
        文件上传
        :param object_name: 文件名称（需要带后缀）
        :param file_path: 文件路径
        """
        file_io = self.file_to_io(file_path)
        length = self.__io_len(file_io)
        resp: ObjectWriteResult = self.client.put_object(
            bucket_name=self.bucket_name,
            object_name=object_name,
            data=file_io,
            length=length,
            *args,
            **kwargs
        )
        return resp.bucket_name, resp.object_name

    @staticmethod
    def __io_len(file_io: IO) -> int:
        current_position = file_io.tell()
        file_io.seek(0)
        data = file_io.read()
        length = len(data)
        file_io.seek(0, current_position)
        return length

    def file_to_io(self, file_path):
        _, file_extension = file_path.rsplit('.', 1)

        if file_extension.lower() == 'docx':
            return self._docx_to_io(file_path)
        if file_extension.lower() == 'pdf':
            return self._pdf_to_io(file_path)

        f = open(file_path, "r", encoding='utf-8')
        return f

    @staticmethod
    def _docx_to_io(file_path):
        doc = Document(file_path)
        io_buffer = io.BytesIO()
        doc.save(io_buffer)
        io_buffer.seek(0)
        return io_buffer

    @staticmethod
    def _pdf_to_io(file_path):
        pdf_document = fitz.open(file_path)
        io_buffer = io.BytesIO()
        pdf_document.save(io_buffer)
        io_buffer.seek(0)
        return io_buffer
