"""
File: log.py
Author: Chuncheng Zhang
Date: 2025-06-09
Copyright & Email: chuncheng.zhang@ia.ac.cn

Purpose:
    Logging for the pdf module.

Functions:
    1. Requirements and constants
    2. Function and class
    3. Play ground
    4. Pending
    5. Pending
"""


# %% ---- 2025-06-09 ------------------------
# Requirements and constants
from datetime import datetime
from loguru import logger

t = datetime.strftime(datetime.now(), '%Y%m%d-%H%M%S')
# %% ---- 2025-06-09 ------------------------
# Function and class

logger.add('log/report-debug.{t}.log',
           level='DEBUG',
           enqueue=True,
           backtrace=True,
           diagnose=True,
           )

logger.add('log/report-info.{t}.log',
           level='INFO',
           enqueue=True,
           backtrace=True,
           diagnose=True,
           )


# %% ---- 2025-06-09 ------------------------
# Play ground


# %% ---- 2025-06-09 ------------------------
# Pending


# %% ---- 2025-06-09 ------------------------
# Pending
