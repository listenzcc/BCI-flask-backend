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
from loguru import logger


# %% ---- 2025-06-09 ------------------------
# Function and class

logger.add('log/report-debug.log',
           level='DEBUG',
           rotation='5 MB',
           retention="2 days",
           enqueue=True,
           backtrace=True,
           diagnose=True,
           compression="zip")

logger.add('log/report-info.log',
           level='INFO',
           rotation='5 MB',
           retention="2 days",
           enqueue=True,
           backtrace=True,
           diagnose=True,
           compression="zip")


# %% ---- 2025-06-09 ------------------------
# Play ground


# %% ---- 2025-06-09 ------------------------
# Pending


# %% ---- 2025-06-09 ------------------------
# Pending
