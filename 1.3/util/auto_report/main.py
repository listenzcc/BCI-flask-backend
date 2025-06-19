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
import markdown
from pathlib import Path
from ollama import Client, ChatResponse


from .util.generator import PDFGenerator
from .util.figure_worker.mk_figure import MkCarFigure1, MkCarFigure2, MkCarFigure3, MkCarFigure4, MkCarFigure5, MkCarFigure6
from .util.figure_worker.mk_figure import MkMouseFigure1, MkMouseFigure2, MkMouseFigure3

import matplotlib.pyplot as plt

# plt.style.use('fivethirtyeight')
plt.style.use('./pacoty.mplstyle')
ollama_host = 'http://172.18.116.140:11434'
ollama_model_name = 'deepseek-r1:32b'

ollama_message_template = {'role': 'user',
                           'content': '''
你是一名心理咨询师，用先进的脑电技术帮助用户监测自己的专注力水平。
请根据以下内容，生成一份关于专注力水平的报告。
输出内容的格式不要用Markdown语法，而是直接生成PDF内容。
内容需要专业、准确、清晰、易懂。 同时要注意语言轻松幽默，避免使用过于专业的术语。
内容包括：1. 专注力水平的概述；2. 专注力水平的影响因素；3. 专注力水平的提升方法。请使用专业的术语和语言，确保报告内容准确、清晰、易懂。篇幅严格控制在400字左右。
以下是科学计算得到的数据与数据的意义描述：
'''}

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

    # for style in ['BodyText', 'CenteredText', 'ImageCaption']:
    #     generator.insert_paragraph(style, 'Subtitle')
    #     if style == 'ImageCaption':
    #         generator.insert_image_with_caption(
    #             Path('./asset/img/img-1.jpg'), 'Example fig')
    #     generator.insert_paragraph(content, style)
    # generator.insert_page_break()

    generator.insert_paragraph('AI助手的建议', style='Subtitle')
    placeholder_idx = len(generator.elements)

    fig_workers = checkout_figworkers(report_name)

    need_saves = {}
    msg = ollama_message_template.copy()

    for f in fig_workers:
        for obj in f.produce():
            # When object is None, use a default image and report
            if obj is None:
                obj = {'buff': Path('./asset/img/404.png'),
                       'report': '404',
                       'name': '404'}

            # Try to read the legend from the processor, add it to the object's legend key
            try:
                obj['legend'] = f.processor.readme_legend
            except:
                obj['legend'] = None

            if legend := obj.get('legend'):
                msg['content'] += f'内容描述:{legend}\n实测数据:{obj["report"]}'

            # If the object has a '_NeedSave' key, update the need_saves dictionary
            if dct := obj.get('_NeedSave'):
                if isinstance(dct, dict):
                    need_saves.update(dct)

            # If the object has a '_NoPDF' key and it is True, skip this object
            if flag := obj.get('_NoPDF'):
                if flag:
                    continue

            # Extract image bytes, report text, and name from the object
            img_bytes = obj['buff']
            report = str(obj['report'])
            name = obj['name']

            # Insert the image with caption and the report text into the PDF
            generator.insert_image_with_caption(img_bytes, name)

            # Insert the legend if it exists
            if legend := obj.get('legend'):
                generator.insert_paragraph(legend)

            # Insert the report text
            generator.insert_paragraph(report)

            # generator.insert_page_break()

    try:
        client = Client(host=ollama_host)
        print(f'连接到 Ollama 服务器: {ollama_host}')
        response: ChatResponse = client.chat(
            model=ollama_model_name,
            messages=[msg]
        )
        ret = response['message']['content']
        lines = ret.split('</think>', 1)[-1].split('\n')
        # print(lines)
        b = generator.elements[placeholder_idx:]
        generator.elements = generator.elements[:placeholder_idx]
        for line in lines:
            if line.strip():
                generator.insert_paragraph(
                    markdown.markdown(line), style='BodyText')
        # html_contents = markdown.markdown('\n'.join(lines))
        # generator.insert_paragraph(html_contents, style='Normal')
        generator.insert_page_break()
        generator.elements.extend(b)
    except Exception as e:
        print(f'连接到 Ollama 服务器失败: {e}')
        generator.insert_paragraph('AI助手忙线中，请稍后再试。')
        pass

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
