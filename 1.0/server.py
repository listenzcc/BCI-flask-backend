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
from pathlib import Path
from omegaconf import OmegaConf
from flask import Flask, Response, request, jsonify

from util.log import logger
from util.known_errors import ERRORS
from util.io import MyReport, DirSystem
from util.machine_learning.attention_calculator.attention_model import AttentionModel
from util.machine_learning.model_storage.model_cache import ModelCache, ChecksumSystem
from util.machine_learning.known_errors import TrainingError, PredictingError

# db
import db.init_connection
from db.train_data_module.train_data_func import get_train_data
from db.train_label_module.train_label_func import get_train_label
from db.predict_module.predict_func import get_predict_data
from db.model_module.model_func import get_latest_model

CONF = OmegaConf.load('./config.yaml')
DS = DirSystem()
DS.load_config(CONF)
MR = MyReport(DS.report_dir)
CS = ChecksumSystem()
MC = ModelCache()

AM = AttentionModel()

app = Flask(__name__)

# %% ---- 2025-05-19 ------------------------
# Function and class


class Message:
    def success_response(self, body: dict) -> Response:
        logger.debug(f'Response success: {body}')
        return jsonify({'status': 'success', 'body': body})

    def error_response(self, body: dict, msg: str) -> Response:
        if isinstance(msg, ERRORS):
            msg = msg.msg
        logger.error(f'Response error: {msg}, {body}')
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
        required_keys = ['name', 'org_id', 'user_id', 'project_name']
        body = request.get_json()
        logger.debug(f'body: {body}')
        assert all(key in body
                   for key in required_keys), 'Missing keys in request body'
    except Exception as e:
        logger.exception(e)
        return MSG.error_response(body={}, msg=ERRORS.request_error), 400

    # Fetch data from db
    try:
        query_kwargs = {
            'org_id': body['org_id'],
            'user_id': body['user_id'],
            'project_name': body['project_name'],
            'name': body['name'],
        }
        data = get_train_data(**query_kwargs)
        label = get_train_label(**query_kwargs)
        print('data', data)
        print('label', label)
        DS.dump_variables('train.dump', data=data, label=label,
                          body=body, query=query_kwargs)
    except Exception as e:
        logger.exception(e)
        return MSG.error_response(body=body, msg=ERRORS.data_fetching_error), 400

    # Train the model
    try:
        # Train the model
        try:
            model = AM.train(data, label)
        except Exception as e:
            logger.exception(e)
            raise e

        info = dict(
            name=body['name'],
            org_id=body['org_id'],
            user_id=body['user_id'],
            project_name=body['project_name'],
        )
        fname = CS.generate_random_filename(info)
        dst = Path(DS.model_dir, fname)
        checksum = CS.save_model(info, model, dst)
        body.update({'model_path': f'{dst.as_posix()},{checksum}',
                    'model_name': model['name']})

        {
            'name': 'name',
            'org_id': 'orgId',
            'user_id': 'userId',
            'project_name': 'projectName',
            'model_path': 'modelPath,CheckSum',
            'model_name': 'modelName'
        }

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
                         'project_name', 'label_content']
        body = request.get_json()
        logger.debug(f'body: {body}')
        assert all(key in body
                   for key in required_keys), 'Missing keys in request body'
    except Exception as e:
        logger.exception(e)
        return MSG.error_response(body={}, msg=ERRORS.request_error), 400

    # Find the model
    try:
        query_kwargs = {
            'org_id': body['org_id'],
            'user_id': body['user_id'],
            'project_name': body['project_name'],
        }
        latest_models = get_latest_model(**query_kwargs)
        DS.dump_variables(
            'predict.dump', query_kwargs=query_kwargs, latest_models=latest_models)
        model_path, checksum = latest_models[-1].split(',')
        model, info, checksum = CS.read_model(model_path, checksum)
        model_record = MC.insert(model, info, checksum)
        model = model_record['model']
    except Exception as e:
        logger.exception(e)
        return MSG.error_response(body=body, msg=ERRORS.model_loading_error), 400

    try:
        kwargs = {
            'org_id': body['org_id'],
            'user_id': body['user_id'],
            'project_name': body['project_name'],
            'name': body['name'],
        }

        # Require label once
        label = body['label_content']

        # Fetch data from db
        # Try maximum 10 times for data when the data is not enough
        for i in range(10):
            try:
                data = get_predict_data(**kwargs)
            except Exception as e:
                logger.exception(e)
                return MSG.error_response(body=body, msg=ERRORS.data_fetching_error), 400
            try:
                # Predict with the model
                predicted = AM.predict(model, data, label)
                logger.debug(f'Predicted: {predicted}')
                body.update(predicted)

                return MSG.success_response(body=body)
            except PredictingError.DataShortageError:
                time.sleep(1)
                continue
    except Exception as e:
        logger.exception(e)
        # If the for loop ends without returning, it means something went wrong
        return MSG.error_response(body=body, msg=ERRORS.inference_error), 400


# %% ---- 2025-05-19 ------------------------
# Play ground
if __name__ == "__main__":
    # Main entry point for debug.
    # Use run_wsgi.ps1 for production usage.
    host = CONF.connection.host
    port = CONF.connection.port
    sys.exit(app.run(host=host, port=port, debug=True))

# %% ---- 2025-05-19 ------------------------
# Pending


# %% ---- 2025-05-19 ------------------------
# Pending
