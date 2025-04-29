from db.operation_module import OperationDao
from db.operation_module.operation import Operation

'''
    create by: shixiaoxia
'''
def query_operation(data_json):
    '''
        获取用户的行为信息
    '''

    operation_dao = OperationDao()


    operation = Operation(org_id=data_json['org_id'],
                          user_id=data_json['user_id'],
                          operation_name=data_json['operation_name'],
                          event=data_json['event'])


    response_result = operation_dao.query_operation(operation)
    print(response_result)

    if response_result:
        user_keys = ["project_name", "train_purpose", "org_id", "user_id", "event", "operation", "create_time"]

        result_list = [dict(zip(user_keys, row)) for row in response_result]
        return result_list
    else:
        return response_result

