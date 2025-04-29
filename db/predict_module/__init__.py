import asyncio
import pickle
from datetime import datetime
from mysql.connector import Error
from db.mysql_module.mysql_conn import MySQLConn
from db.predict_module.predict import Predict

'''
    create by: shixiaoxia
'''

class PredictDao:

    def get_predict_info_by_condition(self, predict):
        '''
        通过条件获取预测信息
        :param predict:
        :return:
        '''


        mysql_conn = MySQLConn()
        cnx = mysql_conn.mysql_pool()

        query_sql = f" SELECT id, org_id, user_id, project_name, name, predict_record, score, create_by, create_time FROM  predict_tb  where  org_id = %s and user_id = %s and project_name = %s and name = %s order by create_time ASC  "
        query_data = []

        query_data.append(predict.org_id)
        query_data.append(predict.user_id)
        query_data.append(predict.project_name)
        query_data.append(predict.name)


        result = None
        try:
            cursor = cnx.cursor()
            cursor.execute(query_sql, query_data)
            result = cursor.fetchall()

        except Error as e:
            result_msg = "获取预测信息，执行失败"
            print(f"{result_msg}, The error '{e}' occurred")

        finally:
            if cnx.is_connected():
                cursor.close()
                cnx.close()
            return result



