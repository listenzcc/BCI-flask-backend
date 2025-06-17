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

from .util.generator import PDFGenerator
from .util.figure_worker.mk_figure import MkCarFigure1, MkCarFigure2, MkCarFigure3, MkCarFigure4, MkCarFigure5, MkCarFigure6
from .util.figure_worker.mk_figure import MkMouseFigure1, MkMouseFigure2, MkMouseFigure3

# %% ---- 2025-06-09 ------------------------
# Function and class


content = '''
万艘龙舸绿丝间，载到扬州尽不还。
应是天教开汴水，一千余里地无山。

尽道隋亡为此河，至今千里赖通波。
若无水殿龙舟事，共禹论功不较多。
'''


def checkout_figworkers(report_name: str):
    workers = []
    if report_name == 'car':
        workers.extend([
            MkCarFigure1(None),
            MkCarFigure2(None),
            MkCarFigure3(None),
            MkCarFigure4(None),
            MkCarFigure5(None),
            MkCarFigure6(None)
        ])
    elif report_name == 'mouse':
        workers.extend([
            MkMouseFigure1(None),
            MkMouseFigure2(None),
            MkMouseFigure3(None)
        ])

    return workers


def generate_report(output_path: Path, report_name: str):
    title = f'Report: {report_name}'

    generator = PDFGenerator()

    generator.insert_title_page(title=title, subtitle='Subtitle')

    for style in ['BodyText', 'CenteredText', 'ImageCaption']:
        generator.insert_paragraph(style, 'Subtitle')
        if style == 'ImageCaption':
            generator.insert_image_with_caption(
                Path('./asset/img/img-1.jpg'), 'Example fig')
        generator.insert_paragraph(content, style)

    generator.insert_page_break()

    fig_workers = checkout_figworkers(report_name)

    need_saves = {}

    for f in fig_workers:
        for obj in f.produce():
            if obj is None:
                obj = {'buff': Path('./asset/img/404.png'),
                       'report': '404',
                       'name': '404'}
            img_bytes = obj['buff']
            report = str(obj['report'])
            name = obj['name']

            if dct := obj.get('_NeedSave'):
                if isinstance(dct, dict):
                    need_saves.update(dct)

            generator.insert_image_with_caption(img_bytes, name)
            try:
                generator.insert_paragraph(f.processor.readme_legend)
            except:
                pass
            generator.insert_paragraph(report)
            # generator.insert_page_break()

    generator.generate(output_path)
    return output_path, need_saves


# %% ---- 2025-06-09 ------------------------
# Play ground

if __name__ == '__main__':
    generate_report(Path('example.pdf'), 'car')
    generate_report(Path('example.pdf'), 'mouse')

# %% ---- 2025-06-09 ------------------------
# Pending


# %% ---- 2025-06-09 ------------------------
# Pending
