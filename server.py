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
from machine_learning.model_worker import MyModel
from machine_learning.report_worker import MyReport

from util.log import logger
from util.known_errors import ERRORS

from db.brain_waves_module.brain_waves_func import get_attention_brain_waves_by_condition, get_non_attention_brain_waves_by_condition

CONF = OmegaConf.load('./config.yaml')
MM = MyModel(CONF.model.path)
MR = MyReport(CONF.report.path)

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
        return MSG.success_response(body={})

    if request.method == 'POST':
        body = request.get_json()
        return MSG.success_response(body=body)

    # Ensure a valid Response is returned for all code paths
    return MSG.error_response(body={}, msg="Invalid request method"), 400


@app.route('/event-stream', methods=['GET'])
def _event_stream():
    def eventStream():
        for i in tqdm(range(30), 'Event streaming'):
            time.sleep(0.03)
            yield f"Date: {time.ctime()}\n\n"

    return Response(eventStream(), mimetype="text/event-stream")


@app.route('/report', methods=['POST'])
def _report():
    '''
    Require to generate the report.
    '''
    # Fetch the input content.
    try:
        body = request.get_json()
        info = dict(
            name=body['name'],
            org_id=body['org_id'],
            user_id=body['user_id'],
            project_name=body['project_name'],
            event=body['event']
        )
        logger.info('1. Got posted data: {}'.format(';'.join(
            [f'{k}: {v}' for k, v in info.items()])))
    except Exception as exc:
        logger.exception(exc)
        err = ERRORS.request_error
        return MSG.error_response(body={}, msg=err.msg), 400

    try:
        report_path, report_name = MR.generate_report(
            info['name'], info['org_id'], info['user_id'], info['project_name'], info['event'])
    except Exception as exc:
        logger.exception(exc)
        err = ERRORS.report_error
        return MSG.error_response(body={}, msg=err.msg), 400

    # Send OK back.
    info.update(dict(report_name=report_name,
                     report_path=report_path,
                     create_by=CONF.project.name,
                     update_by=CONF.project.name))
    return MSG.success_response(body=info), 200


@app.route('/predict', methods=['POST'])
def _predict():
    '''
    Rules:
    1. The body is the received body. If error occurs, just send the body back.
    1.1. In the other word, the body is considered as READ-ONLY.
    2. The info is the running info. If everything is fine, send the info back.
    '''
    # Fetch the input content.
    try:
        body = request.get_json()
        info = dict(
            name=body['name'],
            org_id=body['org_id'],
            user_id=body['user_id'],
            project_name=body['project_name'],
            brain_wave_list=body['brain_wave_list'],
            latest_model_list=body['latest_model_list']
        )
        logger.info('1. Got posted data: {}'.format(';'.join(
            [f'{k}: {v}' for k, v in info.items() if k is not 'brain_wave_list'])))
    except Exception as exc:
        logger.exception(exc)
        err = ERRORS.request_error
        return MSG.error_response(body={}, msg=err.msg), 400

    # Convert the brain_wave_list into numpy array.
    try:
        brain_wave_list = info.pop('brain_wave_list')
        # Require 5s data.
        X = convert_predict_record_into_X(brain_wave_list)
        logger.info(f'2. Got brain_wave_list -> X: {X.shape}')
    except Exception as exc:
        logger.exception(exc)
        err = ERRORS.data_format_error
        return MSG.error_response(body=body, msg=err.msg), 400

    # Get the model.
    try:
        latest_model_list = info.get('latest_model_list')
        latest_model = latest_model_list[-1]
        raw_model_path = latest_model.get('model_path')
        model_name = latest_model.get('model_name')
        model_path, checksum = raw_model_path.split(',')
        MM.prepare_model(model_path, checksum)
        logger.info(f'3. Got model {model_name}@{checksum}:{model_path}')
    except Exception as exc:
        logger.exception(exc)
        err = ERRORS.model_loading_error
        return MSG.error_response(body=body, msg=err.msg), 400

    # The predicting process.
    try:
        pred = MM.predict(checksum, X)
        pred = str(pred)
        logger.info(f'4. Inference has done: {pred}')
    except Exception as exc:
        logger.exception(exc)
        err = ERRORS.inference_error
        return MSG.error_response(body=body, msg=err.msg), 400

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
    # Fetch the input content.
    try:
        body = request.get_json()
        info = dict(
            org_id=body['org_id'],
            user_id=body['user_id'],
            project_name=body['project_name'],
            name=body['name']
        )
        logger.info('1. Got posted data: {}'.format(';'.join(
            [f'{k}: {v}' for k, v in info.items()])))
    except Exception as exc:
        logger.exception(exc)
        err = ERRORS.request_error
        return MSG.error_response(body={}, msg=err.msg), 400

    # Fetch the data and convert into nd-array
    try:
        d1 = get_attention_brain_waves_by_condition(info)
        logger.debug(f'2.1. Got attention_brain_waves {len(d1)}')
        d2 = get_non_attention_brain_waves_by_condition(info)
        logger.debug(f'2.2. Got non_attention_brain_waves {len(d2)}')

        # Require 30s data.
        X_attention = convert_brain_wave_list_into_X(d1, length=30)
        logger.debug(f'2.3. Got X_attention {X_attention.shape}')
        X_non_attention = convert_brain_wave_list_into_X(d2, length=30)
        logger.debug(f'2.4. Got X_non_attention {X_non_attention.shape}')

        # Fold the data at every 5 seconds.
        d = []
        for i in range(6):
            d.append(
                X_attention[:, i*5*SamplingRate:(i+1)*5*SamplingRate])
        X_attention = np.array(d)
        logger.debug(f'2.5. Converted X_attention into {X_attention.shape}')

        d = []
        for i in range(6):
            d.append(
                X_non_attention[:, i*5*SamplingRate:(i+1)*5*SamplingRate])
        X_non_attention = np.array(d)
        logger.debug(
            f'2.6. Converted X_non_attention into {X_non_attention.shape}')

        logger.info(
            f'2. Got X_attention ({X_attention.shape}), X_non_attention ({X_non_attention})')
    except Exception as exc:
        logger.exception(exc)
        err = ERRORS.data_fetching_error
        return MSG.error_response(body=body, msg=err.msg), 400

    # Training process.
    try:
        names = [info['org_id'], info['user_id'],
                 info['project_name'], info['name']]
        trained = MM.train(info, names, X_attention, X_non_attention)
        # Tag the info with trained stuff.
        info.update(trained)
        # Tag the info with created_by signature.
        info.update({
            'created_by': CONF.project.name
        })
        logger.info(f'3. Trained model: {trained}')
    except Exception as exc:
        logger.exception(exc)
        err = ERRORS.training_error
        return MSG.error_response(body=body, msg=err.msg), 400

    # Send OK back.
    return MSG.success_response(body=info), 200


def convert_predict_record_into_X(data):
    '''
    The dct->predict_record should be the list of (channels x points).
    Convert it into ndarray.

    :param data (list): The data in list.

    :return: The ndarray of (channels x points) shape.
    '''
    return np.array(data)


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
