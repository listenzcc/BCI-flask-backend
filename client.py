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
import requests


# %% ---- 2025-03-18 ------------------------
# Function and class
class MyRequest:
    scheme = 'http'
    hostname = 'localhost:5000'

    def post(self, path: str, body: dict) -> requests.Response:
        '''
        Send the post request to the server.

        :param path str: the path to the post request.
        :param body dict: the body of the post request.
        :returns response requests.Response: the response.
        '''
        url = f'{self.scheme}://{self.hostname}/{path}'
        response = requests.post(url, json=body)
        return response

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

    body = {
        'key1': 'value1',
        'key2': 'value2'
    }

    resp = mr.post('echo', body)
    print(f'Status Code: {resp.status_code}')
    print(f'Response JSON: {resp.json()}')

    resp = mr.get('echo')
    print(f'Status Code: {resp.status_code}')
    print(f'Response JSON: {resp.json()}')

    print("Stream starts, listening for messages...")
    mr.get_event_stream('event-stream')
    sys.exit(0)


# %% ---- 2025-03-18 ------------------------
# Pending


# %% ---- 2025-03-18 ------------------------
# Pending
