"""
File: test_error.py
Author: Chuncheng Zhang
Date: 2025-05-26
Copyright & Email: chuncheng.zhang@ia.ac.cn

Purpose:
    Amazing things

Functions:
    1. Requirements and constants
    2. Function and class
    3. Play ground
    4. Pending
    5. Pending
"""


# %% ---- 2025-05-26 ------------------------
# Requirements and constants
from util.machine_learning.known_errors import TrainingError


# %% ---- 2025-05-26 ------------------------
# Function and class
def foo():
    1/0
    raise RuntimeError(TrainingError.LabelError)


# %% ---- 2025-05-26 ------------------------
# Play ground
if __name__ == '__main__':
    try:
        foo()
    except Exception as e:
        print(isinstance(e.args[0](), TrainingError.LabelError))
        print(f'Caught an error: {e}')


# %% ---- 2025-05-26 ------------------------
# Pending


# %% ---- 2025-05-26 ------------------------
# Pending
