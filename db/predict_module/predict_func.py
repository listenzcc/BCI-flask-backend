import json
import pickle
from datetime import datetime

from db.predict_module import PredictDao, Predict

'''
    create by: shixiaoxia
'''

def datetime_to_str(obj):
    """
    将datetime对象转换为字符串
    :param datetime_obj:
    obj.isoformat()
    obj.strftime("%Y-%m-%d %H:%M:%S")
    :return:
    """
    if isinstance(obj, datetime):
        return obj.isoformat()
        # return obj.strftime("%Y-%m-%d %H:%M:%S")


def get_predict_info_by_condition(json_data):
    '''
    获取预测信息
    :return:
    '''
    predict_dao = PredictDao()


    predict = Predict(org_id=json_data['org_id'],
                      user_id=json_data['user_id'],
                      project_name=json_data['project_name'],
                      name=json_data['name'])


    all_rows = predict_dao.get_predict_info_by_condition(predict)
    result_list = []

    user_keys = ["id", "org_id", "user_id", "project_name", "name", "predict_record", "score", "create_by", "create_time"]
    for row in all_rows:
        id, org_id, user_id, project_name, name, predict_record, score, create_by, create_time = row
        # 反序列化二进制数据
        brain_array_data = pickle.loads(predict_record)
        message = {k: v for k, v in zip(user_keys, [id, org_id, user_id, project_name, name, brain_array_data, score, create_by, create_time])}
        result_list.append(json.dumps(message, default=datetime_to_str))

    return result_list
