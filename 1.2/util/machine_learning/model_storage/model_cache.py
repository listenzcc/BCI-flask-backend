import time
import joblib
import random
import hashlib

from typing import Any, Tuple
from pathlib import Path
from ..log import logger


class ModelCache:
    '''Model cache for rapidly predicting.'''
    buffer = {}

    @logger.catch(reraise=True)
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

    @logger.catch(reraise=True)
    def get(self, checksum: str):
        assert checksum in self.buffer, f'No model found with checksum: {checksum}'
        return self.buffer[checksum]


class ChecksumSystem:
    '''Checksum system for model storage.'''

    @logger.catch(reraise=True)
    def generate_random_filename(self, info: dict) -> str:
        '''Generate a checksum for the model info.'''
        t = time.time()
        r = random.random()
        u = f'{info}-{t}-{r}'
        checksum = hashlib.sha256(u.encode()).hexdigest()
        filename = f'{checksum}.model'
        return filename

    @logger.catch(reraise=True)
    def save_model(self, info: dict, model: Any, dst: Path):
        '''
        Save the model.
        Compute a checksum for the model info.
        '''
        dst = Path(dst)
        dst.parent.mkdir(parents=True, exist_ok=True)
        joblib.dump({'model': model, 'info': info}, dst)
        h = hashlib.new('sha256')
        h.update(open(dst, 'rb').read())
        checksum = h.hexdigest()
        logger.info(f'Model saved to {dst}, checksum: {checksum}')
        return checksum

    @logger.catch(reraise=True)
    def read_model(self, model_path: Path, checksum: str) -> Tuple[dict, dict, str]:
        '''
        Prepare the model and info.

        1. Check if the binary file fits the given checksum.
        2. Read the model and info from binary file.
        3. Insert the model and info into the model buffer.

        :param model_path Path: the path of the binary file.
        :param checksum str: the checksum of the binary file.
        :return model: the loaded model.
        :return info: the model info.
        :return checksum: the checksum of the binary file.
        '''
        model_path = Path(model_path)
        h = hashlib.new('sha256')
        h.update(open(model_path, 'rb').read())
        checksum = h.hexdigest()
        assert checksum == checksum, 'The model file fails on matching checksum.'
        dct = joblib.load(model_path)
        model = dct['model']
        info = dct['info']
        logger.info(f'Model loaded from {model_path}, checksum: {checksum}')
        return model, info, checksum
