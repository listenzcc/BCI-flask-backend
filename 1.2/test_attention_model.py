"""
File: test_attention_model.py
Author: Chuncheng Zhang
Date: 2025-05-28
Copyright & Email: chuncheng.zhang@ia.ac.cn

Purpose:
    Test the training and testing of the attention model.

Functions:
    1. Requirements and constants
    2. Function and class
    3. Play ground
    4. Pending
    5. Pending
"""


# %% ---- 2025-05-28 ------------------------
# Requirements and constants
import json
import joblib
import numpy as np
from rich import print
from pathlib import Path

from util.machine_learning.attention_calculator.attention_model import AttentionModel
from util.machine_learning.model_storage.model_cache import ModelCache, ChecksumSystem
from util.machine_learning.known_errors import TrainingError, PredictingError

AM = AttentionModel()
CS = ChecksumSystem()
MC = ModelCache()

# %% ---- 2025-05-28 ------------------------
# Function and class
training_data = json.load(
    open('./example/data-a/train_data.json', encoding='utf-8'))['message']
training_label = json.load(
    open('./example/data-a/train_label.json', encoding='utf-8'))['message']
predicting_data = json.load(
    open('./example/data-a/predict_data.json', encoding='utf-8'))['message']
predicting_result = json.load(
    open('./example/data-a/predict_result.json', encoding='utf-8'))['message']

# %%

obj = joblib.load('./example/train.dump')
training_data1 = obj['data']
training_label1 = obj['label']

# %%
lst = [e['data'] for e in training_data]
d = np.concatenate(lst, axis=1)
print('example', d.shape)

lst = [e['data'] for e in training_data1]
d = np.concatenate(lst, axis=1)
print('real', d.shape)


# %% ---- 2025-05-28 ------------------------
# Play ground

# Train model
print('**** Train model ****')
model = AM.train(training_data, training_label)
print(model)

print('**** Train model ****')
model = AM.train(training_data1, training_label1)
print(model)

# %%

# Save model
print('**** Save model ****')
info = dict(
    name='name',
    org_id='org_id',
    user_id='user_id',
    project_name='project_name',
    event='event'
)
fname = CS.generate_random_filename(info)
dst = Path('test_result/test_attention_model', fname)
checksum = CS.save_model(info, model, dst)
latest_models = [f'{dst.as_posix()},{checksum}']
print(latest_models)

# Load model
print('**** Load model ****')
model_path, checksum = latest_models[-1].split(',')
model, info, checksum = CS.read_model(model_path, checksum)
model_record = MC.insert(model, info, checksum)
model = model_record['model']
print(model)

# Predict with model
print('**** Predict with model ****')
predicted = AM.predict(model, predicting_data, predicting_result)
print(predicted)

# Predict with model without enough data
print('**** Predict with model without enough data ****')
predicting_data['message'] = predicting_data['message'][:5]
predicted = AM.predict(model, predicting_data, predicting_result)
print(predicted)

# %% ---- 2025-05-28 ------------------------
# Pending


# %% ---- 2025-05-28 ------------------------
# Pending
