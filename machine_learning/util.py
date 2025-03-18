"""
File: util.py
Author: Chuncheng Zhang
Date: 2025-03-18
Copyright & Email: chuncheng.zhang@ia.ac.cn

Purpose:
    The utilities for the machine learning algorithms.

Functions:
    1. Requirements and constants
    2. Function and class
    3. Play ground
    4. Pending
    5. Pending
"""


# %% ---- 2025-03-18 ------------------------
# Requirements and constants
import time
import joblib
import hashlib
import numpy as np
from typing import Tuple
from pathlib import Path
from sklearn.svm import SVR
from loguru import logger


# %% ---- 2025-03-18 ------------------------
# Function and class
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


class MyModel:
    inventory_path: Path
    m_cache = ModelCache()

    def __init__(self, inventory_path: Path):
        self.inventory_path = Path(inventory_path)
        self.inventory_path.mkdir(parents=True, exist_ok=True)
        logger.info(f'Initializing with inventory path: {self.inventory_path}')

    def predict(self, checksum: str, X: np.ndarray):
        dct = self.m_cache.get(checksum)
        model = dct['model']
        logger.debug(f'Loaded model: {model}')

        # ! I think it costs 0.3 seconds to predict with the model.
        # ! Make the X.
        time.sleep(0.3)
        X = np.random.random((100, 200))
        pred = model.predict(X)
        return pred

    def train(self, info: dict, X: np.ndarray, y: np.ndarray) -> Tuple[Path, str]:
        logger.debug(f'Train model with {info}')

        # ! I think it costs 1.3 seconds to train a model.
        # ! Make the X & y.
        time.sleep(1.3)
        X = np.random.random((100, 200))
        y = np.random.random((100,))

        # Train the SVR with scipy module.
        model = SVR(kernel='linear')
        model.fit(X, y)

        # Generate the unique filename with md5 algorithm
        localtime = time.time()
        rnd = np.random.random()
        unique = f'{info}-{localtime}-{rnd}'
        filename = hashlib.md5(unique.encode()).hexdigest() + '.bin'
        logger.debug(f'Generated filename: {filename}')

        # Save the model and info into binary file.
        dst = self.inventory_path.joinpath(filename)
        checksum = self.save_model(model, info, dst)

        return dst, checksum

    def save_model(self, model, info: dict, path: Path) -> str:
        '''
        Save the model into binary file.

        :param model object: the trained model.
        :param info dict: the info dictionary.
        :param path Path: the path of the binary file.
        :return str: the checksum of the binary file.
        '''
        joblib.dump({'model': model, 'info': info}, path)
        logger.debug(f'Saved to file: {path}')
        h = hashlib.new('sha256')
        h.update(open(path, 'rb').read())
        checksum = h.hexdigest()
        return checksum

    def prepare_model(self, model_path: Path, checksum: str):
        '''
        Prepare the model and info.

        1. Check if the binary file fits the given checksum.
        2. Read the model and info from binary file.
        3. Insert the model and info into the model buffer.

        :param model_path Path: the path of the binary file.
        :param checksum str: the checksum of the binary file.
        :return model: the loaded model.
        :return info: the model info.
        '''
        model_path = Path(model_path)
        h = hashlib.new('sha256')
        h.update(open(model_path, 'rb').read())
        cs = h.hexdigest()
        assert cs == checksum, 'The model file fails on matching checksum.'
        dct = joblib.load(model_path)
        model = dct['model']
        info = dct['info']
        self.m_cache.insert(model, info, checksum)
        return model, info


# %% ---- 2025-03-18 ------------------------
# Play ground


# %% ---- 2025-03-18 ------------------------
# Pending


# %% ---- 2025-03-18 ------------------------
# Pending
