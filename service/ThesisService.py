# -*- coding:utf-8 -*-
# @FileName  : ThesisService.py
# @Time      : 2023/11/11
# @Author    : LaiJiahao
# @Desc      : 论文生成服务

import uuid
import os

from models.Chain.ThesisChain import ThesisChain
from utils.TexParser import TexParser
from utils.MinIO import MinIOUtil
from loguru import logger
from typing import Tuple


def generate_thesis(keyword: str) -> Tuple:
    random_uuid = uuid.uuid4()
    uuid_str = str(random_uuid)
    t = ThesisChain(uuid_str)
    t.run(keyword=keyword)

    tet_parser = TexParser(uuid_str)
    tet_parser.convert_json_to_tex()
    tet_parser.deploy_tex()

    tet_parser.convert_pdf_to_docx()

    try:
        m = MinIOUtil()
        bucket_name, object_name = m.put_object(f"{uuid_str}.pdf", f"output/{uuid_str}.pdf")
        logger.info(f"PDF文件上传成功, 存储在{bucket_name}/{object_name}")
        bucket_name, object_name = m.put_object(f"{uuid_str}.docx", f"output/{uuid_str}.docx")
        logger.info(f"DOCX文件上传成功, 存储在{bucket_name}/{object_name}")
        return bucket_name, object_name

    except Exception as e:
        logger.error("文件上传失败:", e)
    finally:
        files_list = os.listdir("output")
        for filename in files_list:
            if not (filename.endswith(".pdf") or filename.endswith(".docx") or filename.endswith(".json") or filename.endswith(".tex")):
                os.remove(os.path.join("output", filename))
