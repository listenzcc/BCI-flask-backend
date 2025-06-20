

# %% ---- 2025-06-12 ------------------------
# Requirements and constants
import json
import joblib
import numpy as np
from rich import print
from pathlib import Path

from util.machine_learning.visual_focus_predictor.visual_focus_model import VISUAL_FOCUS_MODEL
from util.machine_learning.model_storage.model_cache import ModelCache, ChecksumSystem
from util.machine_learning.known_errors import TrainingError, PredictingError

VF = VISUAL_FOCUS_MODEL()
CS = ChecksumSystem()
MC = ModelCache()

# %% ---- 2025-05-28 ------------------------
# Function and class
training_data = json.load(
    # 训练数据
    open('./example/data/train_data.json', encoding='utf-8'))['message']
training_label = json.load(
    # 训练label
    open('./example/data/train_label.json', encoding='utf-8'))['message']
predicting_data = json.load(
    # 预测数据
    open('./example/data/predict_data.json', encoding='utf-8'))['message']


# %%

# obj = joblib.load('./example/train.dump')
# training_data1 = obj['data']
# training_label1 = obj['label']

# %%
lst = [e['data'] for e in training_data]
d = np.concatenate(lst, axis=1)
print('example', d.shape)

# lst = [e['data'] for e in training_data1]
# d = np.concatenate(lst, axis=1)
# print('real', d.shape)


# %% ---- 2025-05-28 ------------------------
# Play ground

# Train model
print('**** Train model ****')
model = VF.train(training_data, training_label)
print(model)

print('**** Train model ****')
model = VF.train(training_data, training_label)
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
dst = Path('test_result/test_visual_focus_model', fname)
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
label = '{"type":254,"time":1747646185506}'  # 数据不够的预测label
label = '{"type":254,"time":1747646183506}'  # 数据够的预测label
predicted = VF.predict(model, predicting_data, label)
print(predicted)
