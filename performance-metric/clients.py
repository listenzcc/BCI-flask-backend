"""
File: clients.py
Author: Chuncheng Zhang
Date: 2025-05-22
Copyright & Email: chuncheng.zhang@ia.ac.cn

Purpose:
    Client for localhost testing of the performance metric.

Functions:
    1. Requirements and constants
    2. Function and class
    3. Play ground
    4. Pending
    5. Pending
"""


# %% ---- 2025-05-22 ------------------------
# Requirements and constants
import time
import random
import requests
from tqdm import tqdm
from loguru import logger
from multiprocessing import Process

logger.add('logs/clients.log', rotation='1 MB')
# %% ---- 2025-05-22 ------------------------
# Function and class


def generate_random_bytes(size: int) -> bytes:
    """
    Generate a random byte string of the given size.
    """
    return bytes([random.randint(0, 255) for _ in range(size)])


n = 1024 * 1024 * 10  # 10 MB
total = generate_random_bytes(n)


class Client:
    host = 'localhost'
    port = 5090

    def echo(self, data: dict) -> dict:
        url = f'http://{self.host}:{self.port}/echo'
        response = requests.post(url, json=data)
        return response.json()


def send_batch_requests(client: Client, client_id: int = 0, repeats: int = 10) -> None:
    """
    Send batch requests to the server.
    """
    # n = 1024 * 1024 * random.randint(2, 5)  # 2 ~ 5 MB
    n = 1024 * random.randint(2, 5)  # 2 ~ 5 KB
    for _ in range(repeats):
        data = {
            'n': n,
            'random_bytes': total[:n].hex()
        }
        tic = time.time()
        client.echo(data=data)
        cost = time.time() - tic
        logger.debug(f'Client: {client_id}; Bytes: {n}; Cost: {cost:.4f}')
        time.sleep(0.01)

# %% ---- 2025-05-22 ------------------------
# Play ground


if __name__ == '__main__':
    for i in tqdm(range(100), 'Open clients'):
        client = Client()
        Process(
            target=send_batch_requests,
            args=(client, i, 10),
            daemon=False).start()


# %% ---- 2025-05-22 ------------------------
# Pending


# %% ---- 2025-05-22 ------------------------
# Pending
