"""
File: server.py
Author: Chuncheng Zhang
Date: 2025-05-22
Copyright & Email: chuncheng.zhang@ia.ac.cn

Purpose:
    Server for localhost testing of the performance metric.

Functions:
    1. Requirements and constants
    2. Function and class
    3. Play ground
    4. Pending
    5. Pending
"""


# %% ---- 2025-05-22 ------------------------
# Requirements and constants
import sys
from flask import Flask, Response, request, jsonify

app = Flask(__name__)

# %% ---- 2025-05-22 ------------------------
# Function and class


class Message:
    def success_response(self, body: dict) -> Response:
        return jsonify({'status': 'success', 'body': body})

    def error_response(self, body: dict, msg: str) -> Response:
        return jsonify({'status': 'error', 'msg': msg, 'body': body})


MSG = Message()


@app.route('/echo', methods=['GET', 'POST'])
def _echo():
    if request.method == 'GET':
        return MSG.success_response(body={})

    if request.method == 'POST':
        body = request.get_json()
        return MSG.success_response(body=body)

    # Ensure a valid Response is returned for all code paths
    return MSG.error_response(body={}, msg="Invalid request method"), 400


# %% ---- 2025-05-22 ------------------------
# Play ground
if __name__ == '__main__':
    sys.exit(app.run(host='localhost', port=5090, debug=True))


# %% ---- 2025-05-22 ------------------------
# Pending


# %% ---- 2025-05-22 ------------------------
# Pending
