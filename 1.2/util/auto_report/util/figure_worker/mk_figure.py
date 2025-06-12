"""
File: mk_figure.py
Author: Chuncheng Zhang
Date: 2025-06-11
Copyright & Email: chuncheng.zhang@ia.ac.cn

Purpose:
    Make figure as required.

Functions:
    1. Requirements and constants
    2. Function and class
    3. Play ground
    4. Pending
    5. Pending
"""


# %% ---- 2025-06-11 ------------------------
# Requirements and constants
from .car.fig1_radar.main import Processor as ProcessorCarFig1
from .car.fig2_line.main import Processor as ProcessorCarFig2
from .car.fig3_unbalanced_operation_plot.main import Processor as ProcessorCarFig3
from .car.fig4_attentionhalf.main import Processor as ProcessorCarFig4
from .car.fig5_attentionline.main import Processor as ProcessorCarFig5
from .car.fig6_attentionminutes.main import Processor as ProcessorCarFig6


# %% ---- 2025-06-11 ------------------------
# Function and class
class BaseMkFigure:
    def __init__(self, data):
        self.data = data

    def produce(self):
        pro = self.processor(self.data)

        for obj in pro.process():
            yield obj


class MkCarFigure1(BaseMkFigure):
    processor = ProcessorCarFig1

    def __init__(self, data):
        super().__init__(data)


class MkCarFigure2(BaseMkFigure):
    processor = ProcessorCarFig2

    def __init__(self, data):
        super().__init__(data)


class MkCarFigure3(BaseMkFigure):
    processor = ProcessorCarFig3

    def __init__(self, data):
        super().__init__(data)


class MkCarFigure4(BaseMkFigure):
    processor = ProcessorCarFig4

    def __init__(self, data):
        super().__init__(data)


class MkCarFigure5(BaseMkFigure):
    processor = ProcessorCarFig5

    def __init__(self, data):
        super().__init__(data)


class MkCarFigure6(BaseMkFigure):
    processor = ProcessorCarFig6

    def __init__(self, data):
        super().__init__(data)


# %% ---- 2025-06-11 ------------------------
# Play ground


# %% ---- 2025-06-11 ------------------------
# Pending


# %% ---- 2025-06-11 ------------------------
# Pending
