from db.mysql_module.mysql_conn import MySQLConn

'''
    create by: shixiaoxia
'''

class OperationDao:


    def query_operation(self, operation):
        """
        查询操作记录
        :param operation:
        :return:
        """
        mysql_conn = MySQLConn()
        cnx = mysql_conn.mysql_pool()

        query_operation_sql = " SELECT train_project_tb.project_name, train_project_tb.train_purpose, operation_tb.org_id, operation_tb.user_id, operation_tb.event, operation_tb.operation, operation_tb.create_time  FROM train_project_tb  INNER JOIN operation_tb ON train_project_tb.name = operation_tb.operation_name where 1=1 "

        data_operation = []

        if operation.org_id:
            query_operation_sql += " AND operation_tb.org_id = %s "
            data_operation.append(operation.org_id)

        if operation.user_id:
            query_operation_sql += " AND operation_tb.user_id = %s "
            data_operation.append(operation.user_id)

        if operation.operation_name:
            query_operation_sql += " AND operation_tb.operation_name = %s "
            data_operation.append(operation.operation_name)

        if operation.event:
            query_operation_sql += " AND operation_tb.event = %s "
            data_operation.append(operation.event)

        query_operation_sql += " order by operation_tb.create_time DESC"


        result_msg = "查询操作数据,执行成功"
        result_list = None
        try:
            cursor = cnx.cursor()
            cursor.execute(query_operation_sql, data_operation)
            result_list = cursor.fetchall()
            print(f"{result_msg}")
        except Exception as e:
            result_list = f"查询操作数据,执行失败"
            print(f"{result_list}, The error '{e}' occurred")
        finally:
            if cnx.is_connected():
                cursor.close()
                cnx.close()
            return result_list





