"""
File: server.py
Author: Chuncheng Zhang
Date: 2025-03-18
Copyright & Email: chuncheng.zhang@ia.ac.cn

Purpose:
    Flask server

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
import time
from tqdm.auto import tqdm
from flask import Flask, Response, request, jsonify

app = Flask(__name__)


# %% ---- 2025-03-18 ------------------------
# Function and class
class Message:
    def success_response(self, body: dict) -> Response:
        return jsonify({'status': 'success', 'body': body})

    def error_response(self, body: dict) -> Response:
        return jsonify({'status': 'error', 'body': body})


MSG = Message()


@app.route('/echo', methods=['GET', 'POST'])
def _echo():
    if request.method == 'GET':
        return MSG.success_response(body={}), 200

    if request.method == 'POST':
        body = request.get_json()
        return MSG.success_response(body=body), 200


@app.route('/event-stream', methods=['GET'])
def _event_stream():
    def eventStream():
        for i in tqdm(range(30), 'Event streaming'):
            time.sleep(0.03)
            yield f"Date: {time.ctime()}\n\n"

    return Response(eventStream(), mimetype="text/event-stream")


@app.route('/train', methods=['POST'])
def _train():
    body = request.get_json()
    print(body)
    return MSG.success_response(body=body), 200


# %% ---- 2025-03-18 ------------------------
# Play ground
if __name__ == "__main__":
    # Main entry point for debug.
    # Use run_wsgi.ps1 for production usage.
    host = 'localhost'
    port = 5000
    sys.exit(app.run(host=host, port=port, debug=True))


# %% ---- 2025-03-18 ------------------------
# Pending


# %% ---- 2025-03-18 ------------------------
# Pending
