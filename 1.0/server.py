"""
File: server.py
Author: Chuncheng Zhang
Date: 2025-05-19
Copyright & Email: chuncheng.zhang@ia.ac.cn

Purpose:
    Server for the project.

Functions:
    1. Requirements and constants
    2. Function and class
    3. Play ground
    4. Pending
    5. Pending
"""


# %% ---- 2025-05-19 ------------------------
# Requirements and constants
import sys
import time

from tqdm.auto import tqdm
from omegaconf import OmegaConf
from flask import Flask, Response, request, jsonify

from util.log import logger
from util.known_errors import ERRORS
from util.io import MyReport, MyModel

import db.init_connection
from db.train_data_module.train_data_func import get_train_data
from db.train_label_module.train_label_func import get_train_label
from db.model_module.model_func import get_latest_model

CONF = OmegaConf.load('./config.yaml')
MM = MyModel(CONF.model.path)
MR = MyReport(CONF.report.path)

app = Flask(__name__)

# %% ---- 2025-05-19 ------------------------
# Function and class


class Message:
    def success_response(self, body: dict) -> Response:
        return jsonify({'status': 'success', 'body': body})

    def error_response(self, body: dict, msg: str) -> Response:
        if isinstance(msg, ERRORS):
            msg = msg.msg
        return jsonify({'status': 'error', 'msg': msg, 'body': body})


MSG = Message()


@app.route('/echo', methods=['GET', 'POST'])
def _echo():
    '''Just echo the input'''
    # Echo for the GET request
    if request.method == 'GET':
        return MSG.success_response(body={})

    # Echo for the POST request
    if request.method == 'POST':
        body = request.get_json()
        return MSG.success_response(body=body)

    # Ensure a valid Response is returned for all code paths
    return MSG.error_response(body={}, msg="Invalid request method"), 400


@app.route('/report', methods=['POST'])
def _report():
    '''Generate a report'''
    # Get the request body
    # Check the request body
    try:
        required_keys = ['name', 'org_id', 'user_id', 'project_name', 'event']
        body = request.get_json()
        logger.debug(f'body: {body}')
        assert all(key in body
                   for key in required_keys), 'Missing keys in request body'
    except Exception as e:
        logger.exception(e)
        return MSG.error_response(body={}, msg=ERRORS.request_error), 400

    # Generate the report
    try:
        report_info = MR.generate_report(**body)
        logger.debug(f'Generated report: {report_info}')
        body.update(report_info)
        return MSG.success_response(body=body)
    except Exception as e:
        logger.exception(e)
        return MSG.error_response(body=body, msg=ERRORS.report_error), 400


@app.route('/train', methods=['POST'])
def _train():
    '''Train the model'''
    # Get the request body
    # Check the request body
    try:
        required_keys = ['name', 'org_id', 'user_id', 'project_name', 'event']
        body = request.get_json()
        logger.debug(f'body: {body}')
        assert all(key in body
                   for key in required_keys), 'Missing keys in request body'
    except Exception as e:
        logger.exception(e)
        return MSG.error_response(body={}, msg=ERRORS.request_error), 400

    # TODO: Fetch data from db
    try:
        kwargs = {
            'org_id': body['org_id'],
            'user_id': body['user_id'],
            'project_name': body['project_name'],
            'name': body['name'],
        }
        data = get_train_data(**kwargs)
        label = get_train_label(**kwargs)
    except Exception as e:
        logger.exception(e)
        return MSG.error_response(body=body, msg=ERRORS.data_fetching_error), 400

    # Train the model
    try:
        info = dict(
            name=body['name'],
            org_id=body['org_id'],
            user_id=body['user_id'],
            project_name=body['project_name'],
            event=body['event']
        )
        names = [info['org_id'], info['user_id'],
                 info['project_name'], info['name'], info['event']]
        trained = MM.train(info, names, data, label)
        logger.debug(f'Trained: {trained}')
        body.update(trained)
        return MSG.success_response(body=body)
    except Exception as e:
        logger.exception(e)
        return MSG.error_response(body=body, msg=ERRORS.training_error), 400


@app.route('/predict', methods=['POST'])
def _predict():
    '''Predict with the model'''
    # Get the request body
    # Check the request body
    try:
        required_keys = ['name', 'org_id', 'user_id',
                         'project_name', 'event', 'type']
        body = request.get_json()
        logger.debug(f'body: {body}')
        assert all(key in body
                   for key in required_keys), 'Missing keys in request body'
    except Exception as e:
        logger.exception(e)
        return MSG.error_response(body={}, msg=ERRORS.request_error), 400

    # Find the model
    try:
        kwargs = {
            'org_id': body['org_id'],
            'user_id': body['user_id'],
            'project_name': body['project_name'],
            'type': body['type'],
        }
        latest_models = get_latest_model(**kwargs)
        model_path, checksum = latest_models[-1].split(',')
        MM.prepare_model(model_path, checksum)
        logger.debug(f'Loaded model: {model_path}, {checksum}')
    except Exception as e:
        logger.exception(e)
        return MSG.error_response(body=body, msg=ERRORS.model_loading_error), 400

    # TODO: Fetch data from db
    try:
        kwargs = {
            'org_id': body['org_id'],
            'user_id': body['user_id'],
            'project_name': body['project_name'],
            'name': body['name'],
        }
        data = get_train_data(**kwargs)
    except Exception as e:
        logger.exception(e)
        return MSG.error_response(body=body, msg=ERRORS.data_fetching_error), 400

    # Predict with the model
    try:
        predicted = MM.predict(checksum, data)
        logger.debug(f'Predicted: {predicted}')
        body.update(predicted)
        return MSG.success_response(body=body)
    except Exception as e:
        logger.exception(e)
        return MSG.error_response(body=body, msg=ERRORS.inference_error), 400
# %% ---- 2025-05-19 ------------------------
# Play ground


# %% ---- 2025-05-19 ------------------------
# Pending


# %% ---- 2025-05-19 ------------------------
# Pending
