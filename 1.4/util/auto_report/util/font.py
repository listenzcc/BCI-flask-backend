"""
File: font.py
Author: Chuncheng Zhang
Date: 2025-06-09
Copyright & Email: chuncheng.zhang@ia.ac.cn

Purpose:
    Find and prepare font for pdf file.

Functions:
    1. Requirements and constants
    2. Function and class
    3. Play ground
    4. Pending
    5. Pending
"""


# %% ---- 2025-06-09 ------------------------
# Requirements and constants
import os
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

from .log import logger


# %% ---- 2025-06-09 ------------------------
# Function and class
def register_chinese_font():
    """注册中文字体，返回字体名称"""
    font_name = 'STSong-Light'

    # 尝试使用系统字体
    font_paths = [
        "./asset/msyh.ttc",
        # Windows
        # "C:/Windows/Fonts/msyh.ttc",  # 微软雅黑
        # "C:/Windows/Fonts/simsun.ttc",  # 宋体
        # "C:/Windows/Fonts/simhei.ttf",  # 黑体
        # MacOS
        # "/System/Library/Fonts/STSong.ttf",
        # "/System/Library/Fonts/STHeiti Medium.ttc",
        # Linux
        # "/usr/share/fonts/wenquanyi/wqy-zenhei.ttc",
        # "/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc"
    ]
    try:
        for path in font_paths:
            try:
                font_name = os.path.splitext(os.path.basename(path))[0]
                pdfmetrics.registerFont(TTFont(font_name, path))
                logger.info(f'Using font name: {font_name}')
                return font_name
            except:
                continue

        # 尝试使用reportlab亚洲字体
        from reportlab.pdfbase.cidfonts import UnicodeCIDFont
        pdfmetrics.registerFont(UnicodeCIDFont(font_name))
        logger.info(f'Using default font name: {font_name}')
        return font_name
    except Exception as err:
        logger.exception(err)
        raise Exception("无法注册中文字体，请确保系统安装了中文字体")


# %% ---- 2025-06-09 ------------------------
# Play ground
# font_name = register_chinese_font()


# %% ---- 2025-06-09 ------------------------
# Pending


# %% ---- 2025-06-09 ------------------------
# Pending
