# -*- coding:utf-8 -*-
# @FileName  : TexParser.py
# @Time      : 2023/11/9
# @Author    : LaiJiahao
# @Desc      : Latex格式输出

import json
import re
import os
import subprocess
from pdf2docx import Converter
from loguru import logger


class TexParser:

    def __init__(self, uuid: str):
        self.uuid = uuid

    def deploy_tex(self):
        logger.info("正在编译TEX文件为PDF")
        latex_command = f'latexmk -xelatex -synctex=1 -shell-escape -interaction=nonstopmode -file-line-error {self.uuid}.tex || echo "Warning: LaTeX compilation failed, but continuing script..."'

        try:
            os.chdir('output')
            result = subprocess.run(latex_command,
                                    shell=True,
                                    check=True,
                                    stdout=subprocess.PIPE,
                                    stderr=subprocess.PIPE,
                                    text=True)
            logger.info(f"TEX编译完成")
        except Exception as e:
            logger.error(f"TEX编译失败: {e}")

    def convert_pdf_to_docx(self):
        logger.info("正在讲PDF文件转为DOCX文件")
        cv = Converter(f"output/{self.uuid}.pdf")
        cv.convert(f"output/{self.uuid}.docx", start=0, end=None)
        cv.close()
        logger.info("DOCX文件转换完成")

    def convert_json_to_tex(self):
        logger.info("正在将JSON文件转为TEX文件")
        with open(f"output/{self.uuid}.json", 'r', encoding="utf-8") as f:
            outline_json = json.loads(f.read())

        with open(f"config/default.tex", 'r', encoding='utf-8') as file:
            lines = file.readlines()

        text = ""
        for key, content in outline_json.items():
            index = 0
            title_list = [v for v in key.split(" ") if v]
            level = title_list[0]
            title = title_list[-1]
            line = len(level.split("."))
            content = self.format_content(content)
            if line == 1:
                if index != 0:
                    text += "\n"
                text += self.set_newpage()
                text += self.set_section(title)
                text += content
            if line == 2:
                text += "\n"
                text += self.set_subsection(title)
                text += content
            if line == 3:
                text += "\n"
                text += self.set_subsubsection(title)
                text += content
            index += 1
        for i, line in enumerate(lines):
            if '{latex_content}' in line:
                lines[i] = text + '\n'

        with open(f"output/{self.uuid}.tex", 'w', encoding='utf-8') as file:
            file.writelines(lines)
        logger.info("TEX文件已生成")

    @staticmethod
    def format_content(content: str) -> str:
        content = f"""\n{content.replace('#', '').replace('"', '')}"""
        pattern = re.compile(r'\d+\.\s+(.*?)\n', re.DOTALL)
        matches = pattern.findall(content)

        if matches:
            logger.info("正在格式化TEX表格")
            latex_item = "\\begin{enumerate}\n"
            for match in matches:
                latex_item += f"    \\item {match}\n"
            latex_item += "\\end{enumerate}"
            return latex_item
        return content

    @staticmethod
    def set_section(value):
        return f"\section{{{value}}}"

    @staticmethod
    def set_subsection(value):
        return f"\subsection{{{value}}}"

    @staticmethod
    def set_subsubsection(value):
        return f"\subsubsection{{{value}}}"

    @staticmethod
    def set_newpage():
        return "\\newpage"
