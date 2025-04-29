import json
from datetime import datetime

'''
 create by: shixiaoxia
 预测对象
'''
class Predict:


    def __init__(self, id=None, org_id=None, user_id=None, project_name=None, name=None,
                 predict_record=None, is_predict=None, score=None, comment=None,
                 create_by=None, create_time=None, update_by=None, update_time=None):
        """
        :param id: 唯一id
        :param org_id: 机构Id
        :param user_id: 用户Id
        :param project_name: 项目名称
        :param name: 预测项目项,标识同一个游戏，唯一值，可区分有哪些脑波，预测哪些测试数据
        :param predict_record: 预测数据
        :param is_predict: 是否已预测，1:已预测，0：未预测
        :param score: 分数
        :param comment:备注
        :param create_by:创建人
        :param create_time:创建时间
        :param update_by:更新人
        :param update_time:更新时间
        """
        self.id = id
        self.org_id = org_id
        self.user_id = user_id
        self.project_name = project_name
        self.name = name
        self.predict_record = predict_record
        self.is_predict = is_predict
        self.score = score
        self.comment = comment
        self.create_by = create_by
        self.create_time = create_time
        self.update_by = update_by
        self.update_time = update_time



    def to_dict(self):
        """
        将类对象转换为字典
        :return:
        """
        return {
            "id": self.id,
            "org_id": self.org_id,
            "user_id": self.user_id,
            "project_name": self.project_name,
            "name": self.name,
            "predict_record": self.predict_record,
            "is_predict": self.is_predict,
            "score": self.score,
            "comment": self.comment,
            "create_by": self.create_by,
            "create_time": self.create_time.isoformat() if isinstance(self.create_time,
                                                                      datetime) else self.create_time,
            "update_by": self.update_by,
            "update_time": self.update_time.isoformat() if isinstance(self.update_time,
                                                                      datetime) else self.update_time
        }



    def to_json(self):
        """
        将类对象转换为json
        :return:
        """
        return json.dumps(self.to_dict(), ensure_ascii=False, indent=4)