import json
from datetime import datetime


class BrainWaves:




    def __init__(self, id=None, org_id=None, user_id=None, project_name=None, name=None, brain_record=None, brain_form=None, is_train=None,
                 comment=None, create_by=None, create_time=None, update_by=None, update_time=None):
        '''
        :param id: 唯一id
        :param org_id: 机构Id
        :param user_id: 用户Id
        :param project_name: 项目名称
        :param name: 标识同一个游戏，不同的名称，唯一值，可区分有哪些脑波，预测哪些测试数据
        :param brain_record: 脑波记录
        :param brain_form: 脑波形式：注意力、非注意力
        :param is_train: 是否已训练，1:已训练，0：未训练
        :param comment:备注
        :param create_by:创建人
        :param create_time:创建时间
        :param update_by:更新人
        :param update_time:更新时间
        '''
        self.id = id
        self.org_id = org_id
        self.user_id = user_id
        self.project_name = project_name
        self.name = name
        self.brain_record = brain_record
        self.brain_form = brain_form
        self.is_train = is_train
        self.comment =comment
        self.create_by =create_by
        self.create_time =create_time
        self.update_by =update_by
        self.update_time =update_time


    def to_dict(self):
        return {
            "id": self.id,
            "org_id": self.org_id,
            "user_id": self.user_id,
            "project_name": self.project_name,
            "brain_record": self.brain_record,
            "brain_form": self.brain_form,
            "is_train":self.is_train,
            "comment": self.comment,
            "create_by": self.create_by,
            "create_time": self.create_time.isoformat() if isinstance(self.create_time,
                                                                      datetime) else self.create_time,
            "update_by": self.update_by,
            "update_time": self.update_time.isoformat() if isinstance(self.update_time,
                                                                      datetime) else self.update_time
        }

    def to_json(self):
        return json.dumps(self.to_dict(), ensure_ascii=False, indent=4)