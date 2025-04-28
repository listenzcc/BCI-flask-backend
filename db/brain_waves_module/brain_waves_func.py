from flask import make_response, abort
import pickle
from db.brain_waves_module import BrainWavesDao, BrainWaves


def  get_attention_brain_waves_by_condition(json_data):
    # 根据参数获取训练的脑波数据, 注意力脑波记录
    brain_wave_dao = BrainWavesDao()


    attention_brain_waves = BrainWaves(org_id=json_data['org_id'],
                                       user_id=json_data['user_id'],
                                       project_name=json_data['project_name'],
                                       name=json_data['name'],
                                       is_train=0,
                                       brain_form="注意力")
    print(f"result:{attention_brain_waves.to_json()}")

    attention_all_rows = brain_wave_dao.get_brain_waves_by_condition(attention_brain_waves)
    print(f"训练数据 attention_all_rows：{attention_all_rows}")


    attention = []
    if not attention_all_rows:
        return abort(make_response("训练注意力数据未生成", 10000044))

    user_keys = ["id", "org_id", "user_id", "project_name", "name", "brain_record", "brain_form", "is_train",
                 "create_time"]

    for row in attention_all_rows:
        id, org_id, user_id, project_name, name, brain_record, brain_form, is_train, create_time = row
        # 反序列化二进制数据
        brain_array_data = pickle.loads(brain_record)
        message = {k: v for k, v in zip(user_keys,
                                        [id, org_id, user_id, project_name, name, brain_array_data, brain_form,
                                         is_train, create_time])}
        attention.append(message)

    # print(f"训练数据 attention：{attention}")
    return attention


def  get_non_attention_brain_waves_by_condition(json_data):
    # 根据参数获取训练的脑波数据, 非注意力脑波记录
    brain_wave_dao = BrainWavesDao()

    non_attention_brain_waves = BrainWaves(org_id=json_data['org_id'],
                                           user_id=json_data['user_id'],
                                           project_name=json_data['project_name'],
                                           name=json_data['name'],
                                           is_train=0,
                                           brain_form="非注意力")

    non_attention_all_rows = brain_wave_dao.get_brain_waves_by_condition(non_attention_brain_waves)
    # print(f"训练数据 non_attention_all_rows：{non_attention_all_rows}")

    non_attention = []
    if not non_attention_all_rows:
        return abort(make_response("训练非注意力数据未生成", 10000044))

    user_keys = ["id", "org_id", "user_id", "project_name", "name", "brain_record", "brain_form", "is_train",
                 "create_time"]
    for row in non_attention_all_rows:
        id, org_id, user_id, project_name, name, brain_record, brain_form, is_train, create_time = row
        # 反序列化二进制数据
        brain_array_data = pickle.loads(brain_record)
        message = {k: v for k, v in zip(user_keys,
                                        [id, org_id, user_id, project_name, name, brain_array_data, brain_form,
                                         is_train, create_time])}
        non_attention.append(message)

    # print(f"训练数据 non_attention：{non_attention}")
    return non_attention