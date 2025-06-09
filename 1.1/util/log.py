"""
File: log.py
Author: Chuncheng Zhang
Date: 2025-05-07
Copyright & Email: chuncheng.zhang@ia.ac.cn

Purpose:
    The log for the project.

Functions:
    1. Requirements and constants
    2. Function and class
    3. Play ground
    4. Pending
    5. Pending
"""


# %% ---- 2025-05-07 ------------------------
# Requirements and constants
from loguru import logger


# %% ---- 2025-05-07 ------------------------
# Function and class
logger.add('log/debug.log',
           level='DEBUG',
           rotation='5 MB',
           retention="2 days",
           enqueue=True,
           backtrace=True,
           diagnose=True,
           compression="zip")

logger.add('log/info.log',
           level='INFO',
           rotation='5 MB',
           retention="2 days",
           enqueue=True,
           backtrace=True,
           diagnose=True,
           compression="zip")


# %% ---- 2025-05-07 ------------------------
# Play ground


# %% ---- 2025-05-07 ------------------------
# Pending


# %% ---- 2025-05-07 ------------------------
# Pending
