"""
File: watch-predict.py
Author: Chuncheng Zhang
Date: 2025-04-28
Copyright & Email: chuncheng.zhang@ia.ac.cn

Purpose:
    Watch the predict.txt for its details.

Functions:
    1. Requirements and constants
    2. Function and class
    3. Play ground
    4. Pending
    5. Pending
"""


# %% ---- 2025-04-28 ------------------------
# Requirements and constants
import re
import json
import numpy as np
from rich import print


# %% ---- 2025-04-28 ------------------------
# Function and class
def fix_escapes(json_str):
    return re.sub(r'(?<!\\)\\(?!["\\/bfnrtu])', r'\\\\', json_str)


# %% ---- 2025-04-28 ------------------------
# Play ground
obj = json.loads(fix_escapes(open('./predict.txt', 'r').read()))
display(obj)


# %% ---- 2025-04-28 ------------------------
# Pending
got = json.loads(fix_escapes(obj[0]))
for key, value in got.items():
    print(key, type(value))
    if isinstance(value, list):
        data = np.array(value)
        print(key, type(value), data.shape)


# %% ---- 2025-04-28 ------------------------
# Pending
