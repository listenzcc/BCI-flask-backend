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

from flask import Flask, Response, request, jsonify
from pathlib import Path
from omegaconf import OmegaConf

# Local util
from util.io import MyReport, DirSystem
from util.log import logger
from util.known_errors import ERRORS

# Machine learning
from util.machine_learning.known_errors import TrainingError, PredictingError
from util.machine_learning.model_storage.model_cache import ModelCache, ChecksumSystem
from util.machine_learning.tellme_which_model_to_use import tellme_predict_model, tellme_train_model, checkout_model
from util.machine_learning.attention_calculator.attention_model import AttentionModel

# Auto report
from util.auto_report.main import generate_report

# Local db
try:
    import db.init_connection
    from db.model_module.model_func import get_model
    from db.predict_module.predict_func import get_predict_data
    from db.train_data_module.train_data_func import get_train_data
    from db.train_label_module.train_label_func import get_train_label
except:
    pass

CONF = OmegaConf.load('./config.yaml')

DS = DirSystem()
DS.load_config(CONF)

MC = ModelCache()
CS = ChecksumSystem()

MR = MyReport(DS.report_dir)

app = Flask(__name__)

# %% ---- 2025-05-19 ------------------------
# Function and class


class Message:
    def success_response(self, body: dict) -> Response:
        logger.debug(f'Response success: {body}')
        return jsonify({'status': 'success', 'body': body})

    def error_response(self, body: dict, msg: str) -> Response:
        logger.error(f'Response error: {msg}, {body}')
        return jsonify({'status': 'error', 'msg': str(msg), 'body': str(body)})


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
        return MSG.error_response(body={}, msg=ERRORS.request_error.msg), 400

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
    except Exception as e:
        logger.exception(e)
        return MSG.error_response(body=body, msg=ERRORS.data_fetching_error.msg), 400

    # Determine model name
    try:
        model_names = tellme_train_model(label, body['project_name'])
        # Just make model_names is iterable
        _count = 0
        for _ in model_names:
            _count += 1
            pass
        assert _count > 0, 'Not any model name is determined.'
    except Exception as e:
        logger.exception(e)
        return MSG.error_response(body=body, msg=ERRORS.model_loading_error.msg), 400

    # Checkout model and train it
    trained_models_info = []
    for model_name in model_names:
        logger.debug(f'Training process uses model: {model_name}')
        try:
            Model = checkout_model(model_name)
            training_model = Model()
            logger.debug(f'Using train model: {model_names}')
        except Exception as e:
            logger.exception(e)
            return MSG.error_response(body=body, msg=ERRORS.model_loading_error.msg), 400

        # Train the model
        try:
            # Train the model
            try:
                trained_model: dict = training_model.train(data, label)
                logger.debug(f'Trained model: {model_name}')
            except Exception as e:
                logger.exception(e)
                raise e

            info = dict(
                name=body['name'],
                org_id=body['org_id'],
                user_id=body['user_id'],
                project_name=body['project_name'],
            )
            name = trained_model.get('name', 'Unnamed')
            fname = name+'.'+CS.generate_random_filename(info)
            unique_model_name = f'{name}.{time.time()}'
            dst = Path(DS.model_dir, fname)
            checksum = CS.save_model(info, trained_model, dst)

            # body.update({'model_path': f'{dst.as_posix()},{checksum}',
            #             'model_name': unique_model_name})

            trained_models_info.append({'model_path': f'{dst.as_posix()},{checksum}',
                                        'model_name': unique_model_name})

            __output_example = {
                'name': 'name',
                'org_id': 'orgId',
                'user_id': 'userId',
                'project_name': 'projectName',
                'models': [
                    {'model_path': 'modelPath,CheckSum',
                     'model_name': 'modelName'},
                    {'model_path': 'modelPath,CheckSum',
                     'model_name': 'modelName'},
                ]
            }

            # return MSG.success_response(body=body)
        except Exception as e:
            logger.exception(e)
            dump_body = dict(
                data=data,
                label=label,
                model_name=model_name,
                body=body,
                query=query_kwargs,
                error=f'{e}'
            )
            DS.dump_variables('train-dump', dump_body)
            pass
            # return MSG.error_response(body=body, msg=ERRORS.training_error.msg), 400

        # Done with the model_name
        # If any model is trained, return success msg
        if trained_models_info:
            body.update({'models': trained_models_info})
            return MSG.success_response(body=body)
        # If no model is trained, return error msg
        else:
            return MSG.error_response(body=body, msg=ERRORS.training_error.msg), 400

        continue


@app.route('/report/get', methods=['GET'])
def _report_get():
    body = {}

    report_name = str(request.args.get('report_name'))

    if report_name == 'car':
        data1 = None
        data2 = None
        data3 = None
        data4 = None
        data5 = None
        data6 = None
        report_data = [data1, data2, data3, data4, data5, data6]
    elif report_name == 'mouse':
        data1 = None
        data2 = None
        data3 = None
        report_data = [data1, data2, data3]

    # Generate report
    # report_name = 'car' | 'mouse'
    report_name = 'car'
    output_path = MR.mk_report_path(prefix=f'report-{report_name}')
    path, need_saves = generate_report(output_path, report_name, report_data)
    body.update({'report_path': path.as_posix(),
                'report_name': path.name,
                 })
    body.update(need_saves)

    __output_example = {
        'name': 'name',
        'org_id': 'orgId',
        'user_id': 'userId',
        'project_name': 'projectName',
        'report_path': 'reportPath,CheckSum',
        'report_name': 'reportName'
    }

    return MSG.success_response(body=body)


@app.route('/report', methods=['POST', 'GET'])
def _report():
    '''Generate the report'''
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
        return MSG.error_response(body={}, msg=ERRORS.request_error.msg), 400

    # Generate report
    # report_name = 'car' | 'mouse'
    report_name = 'car'

    try:
        output_path = MR.mk_report_path(prefix=f'report-{report_name}')

        # TODO: Request data
        if report_name == 'car':
            data1 = None
            data2 = None
            data3 = None
            data4 = None
            data5 = None
            data6 = None
            report_data = [data1, data2, data3, data4, data5, data6]
        elif report_name == 'mouse':
            data1 = None
            data2 = None
            data3 = None
            report_data = [data1, data2, data3]
        else:
            raise ValueError(f'Unknown report name: {report_name}')

        path, need_saves = generate_report(
            output_path, report_name, report_data)
        body.update({'report_path': path.as_posix(),
                    'report_name': path.name,
                     'npe': {'npe': None},
                     'file_report': {'file_report': None},
                     'app_report': {'app_report': None}
                     })
        body.update(need_saves)

        __output_example = {
            'name': 'name',
            'org_id': 'orgId',
            'user_id': 'userId',
            'project_name': 'projectName',
            'report_path': 'reportPath,CheckSum',
            'report_name': 'reportName'
        }

        return MSG.success_response(body=body)
    except Exception as e:
        logger.exception(e)
        dump_body = dict(
            body=body,
            report_name=report_name,
            error=f'{e}'
        )
        DS.dump_variables('report-dump', dump_body)
        return MSG.error_response(body=body, msg=ERRORS.report_error.msg), 400


@app.route('/predict', methods=['POST'])
def _predict():
    '''Predict with the model'''
    # Get the request body
    # Check the request body

    try:
        required_keys = ['name', 'org_id', 'user_id',
                         'project_name', 'label_content']
        body = request.get_json()
        # Require label once
        label = body['label_content']
        # logger.debug(f'body: {body}')
        assert all(key in body
                   for key in required_keys), 'Missing keys in request body'
    except Exception as e:
        logger.exception(e)
        return MSG.error_response(body={}, msg=ERRORS.request_error.msg), 400

    # Determine model name
    try:
        model_name: str = tellme_predict_model(label, body['project_name'])
        Model = checkout_model(model_name)
        predicting_model = Model()
        logger.debug(f'Using predict model: {model_name}')
    except Exception as e:
        logger.exception(e)
        return MSG.error_response(body=body, msg=ERRORS.model_loading_error.msg), 400

    # Find the model
    try:
        query_kwargs = {
            'name': body['name'],
            'org_id': body['org_id'],
            'user_id': body['user_id'],
            'project_name': body['project_name'],
        }
        latest_models_raw: list = get_model(**query_kwargs)

        latest_models = []
        for rec in latest_models_raw:
            # Found multiple models
            if m := rec.get('models'):
                latest_models.extend(m)
            # Found single model
            else:
                latest_models.append(rec)
        logger.debug(f'Got latest_models: {latest_models}')

        # Filter the required model
        latest_models = [e for e in latest_models
                         if e.get('model_name').startswith(model_name)]
        model_path, checksum = latest_models[-1]['model_path'].split(',')
        model, info, checksum = CS.read_model(model_path, checksum)
        model_record = MC.insert(model, info, checksum)
        model = model_record['model']
    except Exception as e:
        logger.exception(e)
        return MSG.error_response(body=body, msg=ERRORS.model_loading_error.msg), 400

    data = None
    try:
        predict_body = {
            'org_id': body['org_id'],
            'user_id': body['user_id'],
            'project_name': body['project_name'],
            'name': body['name'],
        }

        # Fetch data from db
        # Try maximum 10 times for data when the data is not enough
        for i in range(10):
            try:
                data = get_predict_data(**predict_body)
            except Exception as e:
                return MSG.error_response(body=body, msg=ERRORS.data_fetching_error.msg), 400
            try:
                # Predict with the model
                predicted = predicting_model.predict(model, data, label)
                logger.debug(f'Predicted: {predicted}')
                body.update({'pred': predicted})
                body.pop('label_content')

                __output_example = {
                    'name': 'name',
                    'org_id': 'orgId',
                    'user_id': 'userId',
                    'project_name': 'projectName',
                    'pred': 'pred'
                }

                return MSG.success_response(body=body)
            except Exception as e:
                time.sleep(1)
                continue
        raise PredictingError.ExceedMaximumPredictingTimes
    except Exception as e:
        logger.exception(e)

        dump_body = dict(
            data=data,
            label=label,
            body=body,
            query_kwargs=query_kwargs,
            latest_models=latest_models,
            error=f'{e}'
        )

        DS.dump_variables('predict-dump', dump_body)

        return MSG.error_response(body=body, msg=ERRORS.inference_error.msg), 400


@app.route('/report_deprecated', methods=['POST'])
def _report_deprecated():
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
        return MSG.error_response(body={}, msg=ERRORS.request_error.msg), 400

    # Generate the report
    try:
        report_info = MR.generate_report(**body)
        logger.debug(f'Generated report: {report_info}')
        body.update(report_info)
        return MSG.success_response(body=body)
    except Exception as e:
        logger.exception(e)
        return MSG.error_response(body=body, msg=ERRORS.report_error.msg), 400


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
