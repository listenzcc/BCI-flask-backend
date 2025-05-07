"""
File: known_errors.py
Author: Chuncheng Zhang
Date: 2025-05-07
Copyright & Email: chuncheng.zhang@ia.ac.cn

Purpose:
    The known errors.

Functions:
    1. Requirements and constants
    2. Function and class
    3. Play ground
    4. Pending
    5. Pending
"""


# %% ---- 2025-05-07 ------------------------
# Requirements and constants


# %% ---- 2025-05-07 ------------------------
# Function and class
class ERRORS:
    class request_error:
        msg = '参数缺失、格式错误或无效请求'
        name = 'Bad Request'
        code = 400

    class data_format_error:
        msg = '脑波或行为数据格式错误'
        name = 'Unprocessable Entity'
        code = 422

    class training_error:
        msg = '模型训练时遇到错误'
        name = 'Internal Server Error'
        code = 500

    class inference_error:
        msg = '模型推断时遇到错误'
        name = 'Internal Server Error'
        code = 500

    class model_loading_error:
        msg = '载入指定模型时遇到错误'
        name = 'Internal Server Error'
        code = 500

    class data_fetching_error:
        msg = '获取时数据遇到错误'
        name = 'Internal Server Error'
        code = 500


# %% ---- 2025-05-07 ------------------------
# Play ground
if __name__ == '__main__':
    e = ERRORS()
    print(e.training_error)
    te = e.training_error
    print(te.msg)
    print(te.name)
    print(te.code)


# %% ---- 2025-05-07 ------------------------
# Pending


# %% ---- 2025-05-07 ------------------------
# Pending
