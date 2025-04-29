

'''
    create by: shixiaoxia
    操作日志对象
'''
import json
from datetime import datetime


class Operation:


    def __init__(self, id=None, org_id=None, user_id=None, operation_name=None, event=None,
                 operation=None, create_by=None, create_time=None, update_by=None, update_time=None):
        """
        :param id: 唯一id
        :param org_id: 机构Id
        :param user_id: 用户Id
        :param operation_name 操作名称
        :param event: 触发事件
        :param operation: 操作数据
        :param create_by:创建人
        :param create_time:创建时间
        :param update_by:更新人
        :param update_time:更新时间
        """
        self.id = id
        self.org_id = org_id
        self.user_id = user_id
        self.operation_name = operation_name
        self.event= event
        self.operation = operation
        self.create_by = create_by
        self.create_time = create_time
        self.update_by = update_by
        self.update_time = update_time


    def to_dict(self):
        """
        将类对象转换为字典
        """
        return {
            "id": self.id,
            "org_id": self.org_id,
            "user_id": self.user_id,
            "operation_name": self.operation_name,
            "event": self.event,
            "operation": self.operation,
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
        """
        return json.dumps(self.to_dict(), ensure_ascii=False, indent=4)

