"""
File: watch-predict-body.py
Author: Chuncheng Zhang
Date: 2025-04-28
Copyright & Email: chuncheng.zhang@ia.ac.cn

Purpose:
    Watch the predict-body.txt for its detail.

Functions:
    1. Requirements and constants
    2. Function and class
    3. Play ground
    4. Pending
    5. Pending
"""


# %% ---- 2025-04-28 ------------------------
# Requirements and constants
import numpy as np
import json


# %% ---- 2025-04-28 ------------------------
# Function and class


# %% ---- 2025-04-28 ------------------------
# Play ground
got = json.load(open('./predict-body.txt'))

for key, value in got.items():
    print(key, type(value))
    if isinstance(value, list):
        data = np.array(value)
        print(key, type(value), data.shape)


# %% ---- 2025-04-28 ------------------------
# Pending


# %% ---- 2025-04-28 ------------------------
# Pending
