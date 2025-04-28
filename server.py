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
import numpy as np

from tqdm.auto import tqdm
from omegaconf import OmegaConf
from flask import Flask, Response, request, jsonify

from interface.util import upload_model_info
from machine_learning.util import MyModel

from db.brain_waves_module.brain_waves_func import get_attention_brain_waves_by_condition, get_non_attention_brain_waves_by_condition

CONF = OmegaConf.load('./config.yaml')
MM = MyModel(CONF.model.path)

app = Flask(__name__)

SamplingRate = 250  # Hz

# %% ---- 2025-03-18 ------------------------
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


@app.route('/predict', methods=['POST'])
def _predict():
    '''
    Rules:
    1. The body is the received body. If error occurs, just send the body back.
    1.1. In the other word, the body is considered as READ-ONLY.
    2. The info is the running info. If everything is fine, send the info back.
    '''
    body = request.get_json()

    # Fetch body with default values
    _default = None  # 'default or None'
    info = dict(
        org_id=body.get('org_id', _default),
        user_id=body.get('user_id', _default),
        project_name=body.get('project_name', _default),
        name=body.get('name', _default),
        brain_wave_list=body.get('brain_wave_list', _default),
        latest_model_list=body.get('latest_model_list', _default)
    )

    # Check if the required parameters are correct.
    if any([v is None for k, v in info.items()]):
        # 400 Bad Request
        msg = "Bad Request, missing parameter(s)."
        return MSG.error_response(body=body, msg=msg), 400

    # Everything is fine.
    # Discard the known large ball.
    if 'brain_wave_list' in info:
        brain_wave_list = info.pop('brain_wave_list')
        # Require 5s data.
        try:
            X = convert_predict_record_into_X(brain_wave_list)
        except Exception as e:
            import traceback
            traceback.print_exc()
            msg = f'Can not convert brain_wave_list into matrix: {brain_wave_list}'
            return MSG.error_response(body=body, msg=msg), 400

    latest_model_list = info.get('latest_model_list')
    if not isinstance(latest_model_list, list) or len(latest_model_list) == 0:
        # 400 Bad Request
        msg = "Bad Request, missing available model(s)."
        return MSG.error_response(body=body, msg=msg), 400

    # Incase something wrong during the predicting process.
    try:
        latest_model = latest_model_list[-1]
        raw_model_path = latest_model.get('model_path')
        model_path, checksum = raw_model_path.split(',')
        MM.prepare_model(model_path, checksum)
        pred = MM.predict(checksum, X)
        pred = str(pred)
    except Exception as e:
        # 500 Internal Server Error
        return MSG.error_response(body=body, msg=f'{e}'), 500

    # Send OK back.
    info.update(dict(pred=pred))
    return MSG.success_response(body=info), 200


@app.route('/train', methods=['POST'])
def _train():
    '''
    Rules:
    1. The body is the received body. If error occurs, just send the body back.
    1.1. In the other word, the body is considered as READ-ONLY.
    2. The info is the running info. If everything is fine, send the info back.
    '''
    body = request.get_json()

    # Fetch body with default values
    _default = None  # 'default or None'
    info = dict(
        org_id=body.get('org_id', _default),
        user_id=body.get('user_id', _default),
        project_name=body.get('project_name', _default),
        name=body.get('name', _default),
        # Remove by protocol change.
        # brain_wave_list_attention=body.get(
        #     'attention', _default),
        # brain_wave_list_non_attention=body.get(
        #     'non_attention', _default)
    )

    # Check if the required parameters are correct.
    if any([v is None for k, v in info.items()]):
        # 400 Bad Request
        msg = "Bad Request, missing parameter(s)."
        return MSG.error_response(body=body, msg=msg), 400

    # Everything is fine.
    # Discard the known large ball.
    if 'brain_wave_list_attention' in info and 'brain_wave_list_non_attention' in info:
        d1 = info.pop('brain_wave_list_attention')
        d2 = info.pop('brain_wave_list_non_attention')
        assert True, 'Should not happen'

    try:
        d1 = get_attention_brain_waves_by_condition(info)
        d2 = get_non_attention_brain_waves_by_condition(info)
        print(info)
        print(d1)
        print(d2)
        # Require 30s data.
        X_attention = convert_brain_wave_list_into_X(d1, length=30)
        X_non_attention = convert_brain_wave_list_into_X(d2, length=30)

        d = []
        for i in range(6):
            d.append(
                X_attention[:, i*5*SamplingRate:(i+1)*5*SamplingRate])
        X_attention = np.array(d)

        d = []
        for i in range(6):
            d.append(
                X_non_attention[:, i*5*SamplingRate:(i+1)*5*SamplingRate])
        X_non_attention = np.array(d)

        print(X_attention.shape, X_non_attention.shape)
    except Exception as e:
        import traceback
        traceback.print_exc()
        # 400 Bad Request
        return MSG.error_response(body=body, msg=f'{e}'), 400

    def train_model():
        '''Train the model.'''
        print(info)
        names = [info['org_id'], info['user_id'],
                 info['project_name'], info['name']]
        trained = MM.train(info, names, X_attention, X_non_attention)
        # Tag the info with trained stuff.
        info.update(trained)
        # Tag the info with created_by signature.
        info.update({
            'created_by': CONF.project.name
        })

        # Deprecated: Upload the model info in async.
        # try:
        #     upload_model_info(info)
        # except:
        #     pass

    # Incase something wrong during the training process.
    try:
        train_model()
    except Exception as e:
        # 400 Bad Request
        import traceback
        traceback.print_exc()
        return MSG.error_response(body=body, msg=f'{e}'), 400

    # Send OK back.
    return MSG.success_response(body=info), 200


def convert_predict_record_into_X(dct: dict):
    '''
    The dct->predict_record should be the list of (channels x points).
    Convert it into ndarray.

    :param dct (dict): The input dict like object containing predict_record.

    :return: The ndarray of (channels x points) shape.
    '''
    return np.array(dct['predict_record'])


def convert_brain_wave_list_into_X(brain_wave_list, fs: int = SamplingRate, length: float = 30):
    '''
    The brain_wave_list should contain (channels x points) matrix and create_time.
        - brain_record: (channels x points) matrix
        - create_time: float
    Convert brain_wave_list into X data.
        1. Sort the brain_wave_list by create_time on ascending order.
        2. Concatenate the brain_record at points axis.
        3. Crop the time points for fs x length points.

    :param brain_wave_list (array): The brain_wave_list data.
    :param fs (int): The sampling rate.
    :param length (int): The required length (in seconds).

    :return: The concatenated data with shape (channels x (fs x length)).
    '''
    # Sort the data as create_time ascending order.
    x = [e['brain_record']
         for e in sorted(brain_wave_list, key=lambda e: e['create_time'])]

    # Concatenate on the time axis.
    X = np.concatenate(x, axis=1)

    # Crop the time points.
    # How many time points are required.
    n = int(fs*length)
    assert X.shape[1] >= n, f'Not enough data to fetch, {X.shape} < {n}'
    X = X[:, -n:]
    return X


# %% ---- 2025-03-18 ------------------------
# Play ground
if __name__ == "__main__":
    # Main entry point for debug.
    # Use run_wsgi.ps1 for production usage.
    host = CONF.connection.host
    port = CONF.connection.port
    sys.exit(app.run(host=host, port=port, debug=True))


# %% ---- 2025-03-18 ------------------------
# Pending


# %% ---- 2025-03-18 ------------------------
# Pending
