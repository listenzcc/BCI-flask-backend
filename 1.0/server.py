"""
File: server.py
Author: Chuncheng Zhang
Date: 2025-05-19
Copyright & Email: chuncheng.zhang@ia.ac.cn

Purpose:
    Server for the project.

Functions:
    1. Requirements and constants
    2. Function and class
    3. Play ground
    4. Pending
    5. Pending
"""


# %% ---- 2025-05-19 ------------------------
# Requirements and constants
import sys
import time

from tqdm.auto import tqdm
from omegaconf import OmegaConf
from flask import Flask, Response, request, jsonify

from util.log import logger
from util.known_errors import ERRORS

CONF = OmegaConf.load('./config.yaml')
MM = MyModel(CONF.model.path)
MR = MyReport(CONF.report.path)

# %% ---- 2025-05-19 ------------------------
# Function and class


# %% ---- 2025-05-19 ------------------------
# Play ground


# %% ---- 2025-05-19 ------------------------
# Pending


# %% ---- 2025-05-19 ------------------------
# Pending
