"""
File: client.py
Author: Chuncheng Zhang
Date: 2025-03-18
Copyright & Email: chuncheng.zhang@ia.ac.cn

Purpose:
    Client for testing purposes.

Functions:
    1. Requirements and constants
    2. Function and class
    3. Play ground
    4. Pending
    5. Pending
"""


# %% ---- 2025-03-18 ------------------------
# Requirements and constants
import sys
import random
import requests
from rich import print
from omegaconf import OmegaConf

CONF = OmegaConf.load('./config.yaml')

# %% ---- 2025-03-18 ------------------------
# Function and class


class MyRequest:
    scheme = 'http'
    hostname = f'{CONF.connection.host}:{CONF.connection.port}'

    def post(self, path: str, body: dict) -> requests.Response:
        '''
        Send the post request to the server.

        :param path str: the path to the post request.
        :param body dict: the body of the post request.
        :returns resp requests.Response: the response.
        '''
        url = f'{self.scheme}://{self.hostname}/{path}'
        print(f'\n\n{url}')
        resp = requests.post(url, json=body)
        print(f'Status Code: {resp.status_code}')
        print(f'Response JSON: {resp.json()}')
        return resp

    def get(self, path: str) -> requests.Response:
        url = f'{self.scheme}://{self.hostname}/{path}'
        response = requests.get(url)
        return response

    def get_event_stream(self, path: str):
        '''
        Connect to the stream endpoint and print messages.

        :param path str: the path to the stream endpoint.
        '''
        url = f'{self.scheme}://{self.hostname}/{path}'
        with requests.get(url, stream=True) as response:
            for line in response.iter_lines():
                if line:
                    print(f"Received Chunk: {line.decode('utf-8')}")
        return


# %% ---- 2025-03-18 ------------------------
# Play ground
if __name__ == '__main__':
    # Make the request object.
    # Send the post request to the server.
    mr = MyRequest()

    # --------------------------------------------------
    body = {
        'org_id': 1,
        'user_id': 2,
        'project_name': 'Project 1',
        'attention': [random.random() for e in range(30*250)],
        'non_attention': [random.random() for e in range(30*250)]
    }

    resp = mr.post('/echo', body)

    # --------------------------------------------------
    resp = mr.get('/echo')

    # --------------------------------------------------
    print("Stream starts, listening for messages...")
    mr.get_event_stream('/event-stream')

    # --------------------------------------------------
    resp = mr.post('/train', body=body)

    dct = resp.json()['body']
    predict_body = {
        'org_id': 1,
        'user_id': 2,
        'project_name': 'Project 1',
        'brain_wave_list': [random.random() for e in range(5*250)],
        'latest_model_list': [{
            'model_path': dct['model_path'],
            'model_name': dct['model_name']
        }]
    }

    # --------------------------------------------------
    for _ in range(10):
        resp = mr.post('/predict', body=predict_body)

    sys.exit(0)


# %% ---- 2025-03-18 ------------------------
# Pending


# %% ---- 2025-03-18 ------------------------
# Pending
