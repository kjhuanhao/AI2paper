# -*- coding:utf-8 -*-
# @FileName  : WordsParser.py
# @Time      : 2023/11/11
# @Author    : LaiJiahao
# @Desc      : 文本解析器

from docx import Document


class WordsParser:
    def __init__(self, uuid: str):
        self.uuid = uuid

    @staticmethod
    def read_docx(file_path):
        doc = Document(file_path)

        for p in doc.paragraphs:
            print(p.text)
        doc.save("output/output.docx")
