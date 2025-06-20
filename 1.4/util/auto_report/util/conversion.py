"""
File: conversion.py
Author: Chuncheng Zhang
Date: 2025-06-09
Copyright & Email: chuncheng.zhang@ia.ac.cn

Purpose:
    Conversion from fig to other format.

Functions:
    1. Requirements and constants
    2. Function and class
    3. Play ground
    4. Pending
    5. Pending
"""


# %% ---- 2025-06-09 ------------------------
# Requirements and constants
from io import BytesIO
from PIL import Image as PILImage
from matplotlib.figure import Figure


# %% ---- 2025-06-09 ------------------------
# Function and class
def fig_to_bytes(fig: Figure):
    buf = BytesIO()
    fig.savefig(buf, format='png')
    buf.seek(0)
    return buf


def fig_to_PIL(fig: Figure):
    return PILImage.open(fig_to_bytes(fig))

# %% ---- 2025-06-09 ------------------------
# Play ground


# %% ---- 2025-06-09 ------------------------
# Pending


# %% ---- 2025-06-09 ------------------------
# Pending
