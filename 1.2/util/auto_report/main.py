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

from .util.conversion import fig_to_bytes
from .util.random_fig import mk_random_fig
from .util.generator import PDFGenerator
from .util.figure_worker.mk_figure import MkCarFigure1, MkCarFigure2, MkCarFigure3, MkCarFigure4, MkCarFigure5, MkCarFigure6

# %% ---- 2025-06-09 ------------------------
# Function and class


content = '''
万艘龙舸绿丝间，载到扬州尽不还。
应是天教开汴水，一千余里地无山。

尽道隋亡为此河，至今千里赖通波。
若无水殿龙舟事，共禹论功不较多。
'''


def generate_report(output_path: Path):
    generator = PDFGenerator()

    generator.insert_title_page(title='Title', subtitle='Subtitle')

    for style in ['BodyText', 'CenteredText', 'ImageCaption']:
        generator.insert_paragraph(style, 'Subtitle')
        if style == 'ImageCaption':
            generator.insert_image_with_caption(
                Path('./asset/img/img-1.jpg'), 'Example fig')
        generator.insert_paragraph(content, style)

    generator.insert_page_break()

    fig1 = MkCarFigure1(None)
    fig2 = MkCarFigure2(None)
    fig3 = MkCarFigure3(None)
    fig4 = MkCarFigure4(None)
    fig5 = MkCarFigure5(None)
    fig6 = MkCarFigure6(None)
    for f in [fig1, fig2, fig3, fig4, fig5, fig6]:
        for obj in f.produce():
            img_bytes = obj['buff']
            report = str(obj['report'])
            name = obj['name']
            generator.insert_image_with_caption(img_bytes, name)
            try:
                generator.insert_paragraph(f.processor.readme_legend)
            except:
                pass
            generator.insert_paragraph(report)
            # generator.insert_page_break()

    generator.insert_paragraph('表格')
    data = [
        ('职位名称', '平均薪资', '较上年增长率'),
        ('Trump', '18.5K', '25%'),
        ('Musk', '25.5K', '14%'),
        ('SomeOne', '29.3K', '10%')
    ]
    generator.insert_table(*data)
    generator.insert_page_break()

    for i in range(5):
        img_bytes = fig_to_bytes(mk_random_fig())
        generator.insert_image_with_caption(
            img_bytes, f'Fig. {i} Image caption')
    generator.generate(output_path)


# %% ---- 2025-06-09 ------------------------
# Play ground

if __name__ == '__main__':
    generate_report(Path('example.pdf'))

# %% ---- 2025-06-09 ------------------------
# Pending


# %% ---- 2025-06-09 ------------------------
# Pending
