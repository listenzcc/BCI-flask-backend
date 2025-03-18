"""
File: util.py
Author: Chuncheng Zhang
Date: 2025-03-18
Copyright & Email: chuncheng.zhang@ia.ac.cn

Purpose:
    Utility functions for connecting with the remote end.

Functions:
    1. Requirements and constants
    2. Function and class
    3. Play ground
    4. Pending
    5. Pending
"""


# %% ---- 2025-03-18 ------------------------
# Requirements and constants
import requests


# %% ---- 2025-03-18 ------------------------
# Function and class

def upload_model_info(info: dict):
    '''
    2.存储模型接口
    POST 	http://192.168.3.138:5000/api/model/insert

    参数：

    {
        "org_id":"0001",	# 机构id
        "user_id":"0003",	# 用户编码
        "project_name":"xxx",	#项目名称
        "model_name":"模型5",	#模型名称
        "model_path":"xxx",	#模型存放地址
        "create_by":"admin",	#创建人
        "update_by":"admin"	#更新人
    }

    '''
    url = "http://192.168.3.138:5000/api/model/insert"
    return requests.post(url, json=info, timeout=0.1)


# %% ---- 2025-03-18 ------------------------
# Play ground


# %% ---- 2025-03-18 ------------------------
# Pending


# %% ---- 2025-03-18 ------------------------
# Pending
