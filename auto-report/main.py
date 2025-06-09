"""
File: main.py
Author: Chuncheng Zhang
Date: 2025-06-09
Copyright & Email: chuncheng.zhang@ia.ac.cn

Purpose:
    Main script for automatically generate auto report.

Functions:
    1. Requirements and constants
    2. Function and class
    3. Play ground
    4. Pending
    5. Pending
"""


# %% ---- 2025-06-09 ------------------------
# Requirements and constants
from pathlib import Path
from reportlab.pdfbase import pdfmetrics  # 注册字体
from reportlab.pdfbase.ttfonts import TTFont  # 字体类
from reportlab.platypus import Table, SimpleDocTemplate, Paragraph, Image  # 报告内容相关类
from reportlab.lib.pagesizes import letter  # 页面的标志尺寸(8.5*inch, 11*inch)
from reportlab.lib.styles import getSampleStyleSheet  # 文本样式
from reportlab.lib import colors  # 颜色模块
from reportlab.lib.units import cm, inch  # 单位：cm, inch

from plot.conversion import fig_to_bytes
from plot.random_fig import mk_random_fig

from util.generator import PDFGenerator

# %% ---- 2025-06-09 ------------------------
# Function and class

# Registering a font named 'simfang' with the file 'simfang.ttf'.
pdfmetrics.registerFont(TTFont('simfang', 'simfang.ttf'))

style_list = getSampleStyleSheet()


def insert_full_title(title_name='Title Name'):
    """
    This function takes in a title name and returns the full title name.

    :param title_name: The name of the title you want to insert
    """
    font_ = style_list['Heading1']
    font_.fontName = 'simfang'
    font_.fontSize = 18
    font_.leading = 50
    font_.textColor = colors.green
    font_.alignment = 1
    font_.bold = True
    return Paragraph(title_name, font_)


def insert_letter_title(letter_name='Letter Name'):
    """
    :param : The name of the letter you want to insert
    """
    font_ = style_list['Normal']
    font_.fontName = 'simfang'
    font_.fontSize = 15
    font_.leading = 30
    font_.textColor = colors.red
    return Paragraph(letter_name, font_)


def insert_text(text='Text'):
    """
    This function inserts text into the current document

    :param text: The text to insert
    """
    font_ = style_list['Normal']
    font_.fontName = 'simfang'
    font_.fontSize = 12
    font_.wordWrap = 'CJK'
    font_.alignment = 0
    font_.firstLineIndent = 32
    font_.leading = 25
    return Paragraph(text, font_)


def insert_table(*args):
    """
    It inserts a table into the database.
    """
    col_width = 120
    style = [
        ('FONTNAME', (0, 0), (-1, -1), 'simfang'),  # 字体
        ('FONTSIZE', (0, 0), (-1, 0), 12),  # 第一行的字体大小
        ('FONTSIZE', (0, 1), (-1, -1), 10),  # 第二行到最后一行的字体大小
        ('BACKGROUND', (0, 0), (-1, 0), '#d5dae6'),  # 设置第一行背景颜色
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),  # 第一行水平居中
        ('ALIGN', (0, 1), (-1, -1), 'LEFT'),  # 第二行到最后一行左右左对齐
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),  # 所有表格上下居中对齐
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.darkslategray),  # 设置表格内文字颜色
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),  # 设置表格框线为grey色，线宽为0.5
    ]
    table = Table(args, colWidths=col_width, style=style)
    return table


def insert_image(image_path_or_bytes=None):
    """
    > This function inserts an image into the notebook

    :param image_path_or_bytes:
        The path to the image you want to insert.
        Or the bytes can be converted to Image
    """
    img = Image(image_path_or_bytes)
    img.drawWidth = 6 * inch
    img.drawHeight = 4 * inch
    return img


# %% ---- 2025-06-09 ------------------------
# Play ground
# A special variable in Python that evaluates to `True` if the module is being run as the main program.
if __name__ == '__main__':
    generator = PDFGenerator()

    generator.add_title_page(title='Title', subtitle='Subtitle')
    generator.add_paragraph('fu83niubrnfuygbafyugdggggggggggggggg'*4)
    generator.add_page_break()
    for i in range(5):
        img_bytes = fig_to_bytes(mk_random_fig())
        generator.add_image_with_caption(
            img_bytes, f'Fig. {i} Image caption', 6, 4)
    generator.generate(Path('example1.pdf'))

    pdf_ = list()

    pdf_.append(insert_full_title('数据测试报告'))
    pdf_.append(insert_text(
        'Python 是一门编程语言。 您可以在服务器上使用 Python 来创建 Web 应用程序。通过实例学习 我们的 TIY 编辑器使学习 Python 变得简单,它能够同时显示代码和结果。 '))

    for _ in range(3):
        img_bytes = fig_to_bytes(mk_random_fig())
        pdf_.append(insert_image(img_bytes))

    pdf_.append(insert_letter_title('数据内容展示：'))
    data = [
        ('职位名称', '平均薪资', '较上年增长率'),
        ('数据分析师', '18.5K', '25%'),
        ('高级数据分析师', '25.5K', '14%'),
        ('资深数据分析师', '29.3K', '10%')
    ]
    pdf_.append(insert_table(*data))

    doc = SimpleDocTemplate('example.pdf', pagesize=letter)
    doc.build(pdf_)


# %% ---- 2025-06-09 ------------------------
# Pending


# %% ---- 2025-06-09 ------------------------
# Pending
