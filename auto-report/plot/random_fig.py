"""
File: random_fig.py
Author: Chuncheng Zhang
Date: 2025-06-09
Copyright & Email: chuncheng.zhang@ia.ac.cn

Purpose:
    Generate random figure.

Functions:
    1. Requirements and constants
    2. Function and class
    3. Play ground
    4. Pending
    5. Pending
"""


# %% ---- 2025-06-09 ------------------------
# Requirements and constants
import numpy as np
import matplotlib.pyplot as plt


# %% ---- 2025-06-09 ------------------------
# Function and class
def mk_random_fig(width: float = 6, height: float = 4):
    pos = np.random.randn(100, 2)
    fig = plt.figure(figsize=(width, height))
    fig, ax = plt.subplots(1, 1, figsize=(width, height))
    ax.scatter(pos[:, 0], pos[:, 1])
    ax.set_title('Random points (100)')
    fig.tight_layout()
    print(type(fig))
    return fig


# %% ---- 2025-06-09 ------------------------
# Play ground


# %% ---- 2025-06-09 ------------------------
# Pending


# %% ---- 2025-06-09 ------------------------
# Pending
