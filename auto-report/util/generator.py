"""
File: generator.py
Author: Chuncheng Zhang
Date: 2025-06-09
Copyright & Email: chuncheng.zhang@ia.ac.cn

Purpose:
    Generator for the pdf file.

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
import os
import hashlib
import matplotlib.pyplot as plt

from io import BytesIO
from datetime import datetime
from PIL import Image as PILImage

from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import Paragraph, Spacer, Image, PageBreak, BaseDocTemplate, Frame, PageTemplate

from .font import register_chinese_font
from .log import logger


# %% ---- 2025-06-09 ------------------------
# Function and class
def mk_sha256(b: bytes):
    """Convert bytes into sha256 representation string.

    Args:
        b (bytes): The input bytes.

    Returns:
        str: The sha256 representation string.
    """
    m = hashlib.sha256()
    m.update(b'listenzcc')
    m.update(b)
    return m.hexdigest()


def setup_styles(font_name):
    """设置样式表"""
    styles = getSampleStyleSheet()

    # 修改现有样式使用中文字体
    for style_name in styles.byName:
        styles[style_name].fontName = font_name

    # 添加自定义样式
    custom_styles = {
        'Title': {
            'parent': styles['Heading1'],
            'fontSize': 24,
            'leading': 28,
            'alignment': TA_CENTER,
            'spaceAfter': 20,
            'textColor': colors.darkblue,
            'fontName': font_name
        },
        'Subtitle': {
            'parent': styles['Heading2'],
            'fontSize': 14,
            'leading': 18,
            'alignment': TA_CENTER,
            'spaceAfter': 15,
            'textColor': colors.darkblue,
            'fontName': font_name
        },
        'BodyText': {
            'parent': styles['BodyText'],
            'fontSize': 12,
            'leading': 15,
            'alignment': TA_LEFT,
            'spaceAfter': 10,
            'fontName': font_name
        },
        'CenteredText': {
            'parent': styles['Normal'],
            'fontSize': 12,
            'leading': 15,
            'alignment': TA_CENTER,
            'spaceAfter': 10,
            'fontName': font_name
        },
        'ImageCaption': {
            'parent': styles['Italic'],
            'fontSize': 10,
            'leading': 12,
            'alignment': TA_CENTER,
            'spaceBefore': 5,
            'spaceAfter': 15,
            'fontName': font_name
        },
        'Stopper': {
            'parent': styles['Normal'],
            'fontSize': 14,
            'leading': 10,
            'alignment': TA_CENTER,
            'spaceBefore': 10,
            'fontName': font_name,
            'textColor': colors.darkred,
        }
    }

    for style_name, style_params in custom_styles.items():
        if style_name in styles:
            logger.warning(
                f'Define {style_name}, but the sample style already has it, so I am ignoring it.')
        else:
            styles.add(ParagraphStyle(name=style_name, **style_params))
            logger.debug(f'Using style: {style_name} = {style_params}')

    return styles


class PDFGeneratorBase:
    font_name = register_chinese_font()
    page_size = A4
    styles = setup_styles(font_name)

    def __init__(self):
        self.date = datetime.now().isoformat()
        self.serial = mk_sha256(self.date.encode('utf-8')).upper()
        self.mk_doc()

        # The elements grow as the report is drawn.
        self.elements = []

    def generate(self, path: Path):
        self.doc.build(self.elements)
        logger.debug(f'Built doc with {len(self.elements)} elements')
        path.parent.mkdir(parents=True, exist_ok=True)
        with open(path, 'wb') as f:
            f.write(self.buff.getvalue())
        logger.info(f'Wrote file: {path}')
        return path

    def mk_doc(self):
        self.buff = BytesIO()
        self.doc = BaseDocTemplate(
            self.buff,
            pagesize=self.page_size,
            rightMargin=72,
            leftMargin=72,
            topMargin=72,
            bottomMargin=72
        )

        content_frame = Frame(
            self.doc.leftMargin,
            self.doc.bottomMargin + 0.5 * inch,  # Leave space for footer
            self.doc.width,
            self.doc.height - 0.5 * inch,
            id='content'
        )
        footer_frame = Frame(
            self.doc.leftMargin,
            self.doc.bottomMargin,
            self.doc.width,
            0.5 * inch,
            id='footer'
        )
        self.doc.addPageTemplates([PageTemplate(
            id='MyPage1',
            frames=[content_frame, footer_frame],
            onPage=self._render_page)
        ])
        return self.doc

    def _render_page(self, canvas: canvas.Canvas, doc):
        """Customizes the first page (adds footer at the bottom)."""
        canvas.saveState()
        # Header text
        header_text = f'序列号：{self.serial.upper()}'  # "Python自动报告生成 - 仅供学习使用"
        canvas.setFont(self.font_name, 8)
        canvas.setFillColor('gray')
        canvas.drawString(
            self.doc.leftMargin,
            self.page_size[1] - 0.5 * inch,  # Ensure header is at the top.
            header_text
        )
        # Draw line below the header
        canvas.setStrokeColor('gray')
        canvas.line(
            self.doc.leftMargin,
            self.page_size[1] - 0.55 * inch,
            self.page_size[0] - self.doc.rightMargin,
            self.page_size[1] - 0.55 * inch
        )
        # Page number
        current_page = doc.page
        page_number = f"第 {current_page} 页"
        canvas.drawCentredString(
            self.page_size[0] / 2.0,
            0.35 * inch,  # Page number is at the bottom.
            page_number
        )
        canvas.restoreState()
        return


class PDFGenerator(PDFGeneratorBase):
    def __init__(self):
        super().__init__()

    def add_image_with_caption(self, path_or_bytes, caption: str, width: float = 0, height: float = 0):
        """
        This function inserts an image into the doc.

        :param image_path_or_bytes:
            The path to the image you want to insert.
            Or the bytes can be converted to Image
        """
        img = Image(path_or_bytes)
        if width > 0:
            img.drawWidth = width * inch
        if height > 0:
            img.drawHeight = height * inch
        self.elements.append(img)
        self.elements.append(Paragraph(caption, self.styles['ImageCaption']))
        # 添加一些间距
        self.elements.append(Spacer(1, 0.3*inch))
        logger.debug(f'Added {img}, {caption}')
        pass

    def add_title_page(self, title: str, subtitle: str = ''):
        """添加标题页"""
        # Title
        self.elements.append(Spacer(1, 1*inch))
        self.elements.append(Paragraph(title, self.styles['Title']))

        # Subtitle
        if subtitle:
            self.elements.append(Paragraph(subtitle, self.styles['Subtitle']))

        # Others
        self.elements.append(Spacer(1, 2*inch))
        blank = '_' * len(self.date)
        self.elements.append(
            Paragraph(f"情况A: {blank}", self.styles['CenteredText']))
        self.elements.append(
            Paragraph(f"情况B: {blank}", self.styles['CenteredText']))
        self.elements.append(
            Paragraph(f"情况C: {blank}", self.styles['CenteredText']))
        self.elements.append(
            Paragraph(f'日期：{self.date}', self.styles['CenteredText']))

        # Segment
        self.add_page_break()
        logger.debug(f'Added title page: {title}, {subtitle}')
        return

    def add_paragraph(self, text: str, style='BodyText'):
        """添加段落"""
        self.elements.append(Paragraph(text, self.styles[style]))
        self.elements.append(Spacer(1, 0.2*inch))
        logger.debug(f'Added text: {text[:20]}...')
        return

    def add_page_break(self):
        self.elements.append(PageBreak())
        logger.debug('Added page break')
        return
# %% ---- 2025-06-09 ------------------------
# Play ground


# %% ---- 2025-06-09 ------------------------
# Pending


# %% ---- 2025-06-09 ------------------------
# Pending
