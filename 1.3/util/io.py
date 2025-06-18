"""
File: io.py
Author: Chuncheng Zhang
Date: 2025-05-19
Copyright & Email: chuncheng.zhang@ia.ac.cn

Purpose:
    File io utilities.

Functions:
    1. Requirements and constants
    2. Function and class
    3. Play ground
    4. Pending
    5. Pending
"""


# %% ---- 2025-05-19 ------------------------
# Requirements and constants
import time
import joblib
from pathlib import Path
from .log import logger


# %% ---- 2025-05-19 ------------------------
# Function and class
class DirSystem:
    root: Path
    model_dir: Path
    report_dir: Path
    dumps_dir: Path

    @logger.catch(reraise=True)
    def load_config(self, config):
        self.root = self.mkdir(Path(config.project.dir))
        self.model_dir = self.mkdir(
            Path(config.project.dir, config.model.subdir))
        self.report_dir = self.mkdir(
            Path(config.project.dir, config.report.subdir))
        self.dumps_dir = self.mkdir(
            Path(config.project.dir, config.dumps.subdir))

    @logger.catch(reraise=True)
    def mkdir(self, dir: Path):
        if dir.is_dir():
            logger.info(f'Dir exists: {dir}')
        else:
            dir.mkdir(parents=True, exist_ok=True)
            logger.info(f'Mkdir: {dir}')
        return dir

    @logger.catch
    def dump_variables(self, dump_name: str, dump_body: dict):
        from datetime import datetime
        import random
        day = datetime.now().strftime('%Y%m%d')
        detail = datetime.now().strftime('%Y%m%d-%H%M%S')
        path = self.dumps_dir.joinpath(
            f'{day}', f'{dump_name}.{detail}-{random.random():0.8f}.dump')
        path.parent.mkdir(parents=True, exist_ok=True)
        joblib.dump(dump_body, path)
        logger.debug(f'Dump variables: {list(dump_body.keys())} -> {path}')
        return dump_body


class MyReport:
    directory: Path

    def __init__(self, directory: Path):
        self.directory = Path(directory)
        self.directory.mkdir(parents=True, exist_ok=True)
        logger.info(f'Initialize with directory: {directory}')

    def mk_report_path(self, prefix='report'):
        rnd = time.time()
        return self.directory.joinpath(f'{prefix}-{rnd}.pdf')


class ModelCache:
    '''Model cache for rapidly predicting.'''
    buffer = {}

    def insert(self, model, info, checksum: str):
        if checksum not in self.buffer:
            self.buffer[checksum] = {
                'model': model,
                'info': info,
                'checksum': checksum
            }
            logger.debug(f'Cache update with new model: {info}, {checksum}')
        else:
            logger.debug(f'Cache hit: {checksum}')
        return self.buffer[checksum]

    def get(self, checksum: str):
        assert checksum in self.buffer, f'No model found with checksum: {checksum}'
        return self.buffer[checksum]


# %% ---- 2025-05-19 ------------------------
# Play ground


# %% ---- 2025-05-19 ------------------------
# Pending


# %% ---- 2025-05-19 ------------------------
# Pending
