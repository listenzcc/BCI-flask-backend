"""
File: known_errors.py
Author: Chuncheng Zhang
Date: 2025-05-22
Copyright & Email: chuncheng.zhang@ia.ac.cn

Purpose:
    Known errors in machine learning modules.

Functions:
    1. Requirements and constants
    2. Function and class
    3. Play ground
    4. Pending
    5. Pending
"""


# %% ---- 2025-05-22 ------------------------
# Requirements and constants


# %% ---- 2025-05-22 ------------------------
# Function and class
class MyError:
    def __init__(self):
        super().__init__(self.name)


class ModelLoadingError:
    class NameError(MyError, Exception):
        msg = '模型名称错误'
        name = 'Model Name Error'
        code = 1311


class TrainingError:
    class LabelError(MyError, Exception):
        msg = '标签错误，标签中不包含有效类别'
        name = 'Label Error'
        code = 1411

    class DataShortageError(MyError, Exception):
        msg = '数据不足，无法进行训练'
        name = 'Data Shortage Error'
        code = 1412

    class DataFormatError(MyError, Exception):
        msg = '数据格式错误，无法根据指定标签进行训练'
        name = 'Data Format Error'
        code = 1413

    class ModelTrainingError(MyError, Exception):
        msg = '模型训练错误，无法进行训练'
        name = 'Model Error'
        code = 1414

    class DataLabelMissMatch(MyError, Exception):
        msg = '数据与标签不匹配'
        name = 'Data & Label Miss Match Error'
        code = 1415

    class ProjectNameError(MyError, Exception):
        msg = '项目名称错误'
        name = 'Project Name Error'
        code = 1416

    class UnExceptedError(MyError, Exception):
        msg = '模型训练时遇到错误，但此错误不在已知错误列表中'
        name = 'UnExcepted Error'
        code = 1410


class PredictingError:
    class LabelError(MyError, Exception):
        msg = '标签错误，标签中不包含有效类别'
        name = 'Label Error'
        code = 1511

    class DataShortageError(MyError, Exception):
        msg = '数据不足，无法进行预测'
        name = 'Data Storage Error'
        code = 1512

    class DataFormatError(MyError, Exception):
        msg = '数据格式错误，无法进行预测'
        name = 'Data Format Error'
        code = 1513

    class ModelError(MyError, Exception):
        msg = '模型错误，无法进行预测'
        name = 'Model Error'
        code = 1514

    class ExceedMaximumPredictingTimes(MyError, Exception):
        msg = '模型预测时尝试的次数超过阈值'
        name = 'Exceed Maximum Predicting Times Error'
        code = 1515

    class DataLabelMissMatch(MyError, Exception):
        msg = '数据与标签不匹配'
        name = 'Data & Label Miss Match Error'
        code = 1516

    class ProjectNameError(MyError, Exception):
        msg = '项目名称错误'
        name = 'Project Name Error'
        code = 1517

    class UnExceptedError(MyError, Exception):
        msg = '模型预测时遇到错误，但此错误不在已知错误列表中'
        name = 'UnExcepted Error'
        code = 1510


# %% ---- 2025-05-22 ------------------------
# Play ground
if __name__ == '__main__':
    def foo():
        raise TrainingError.DataFormatError

    try:
        foo()
    except Exception as e:
        print(e)
        print(e.msg)
        print(e.name)
        print(e.code)
        raise e

# %% ---- 2025-05-22 ------------------------
# Pending


# %% ---- 2025-05-22 ------------------------
# Pending
