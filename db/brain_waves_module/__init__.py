from db.brain_waves_module.brain_waves import BrainWaves
from db.mysql_module.mysql_conn import MySQLConn
from mysql.connector import Error

class BrainWavesDao:


    def get_brain_waves_by_condition(self, brain_waves):
        '''
        通过name和获取brain_form获取脑波记录进行训练
        :param brain_waves:
        :return:
        '''


        mysql_conn = MySQLConn()
        cnx = mysql_conn.mysql_pool()

        brain_waves_sql = f"select bw.id, bw.org_id, bw.user_id, bw.project_name, bw.name, bw.brain_record, bw.brain_form, bw.is_train, bw.create_time from brain_waves_tb as bw where bw.org_id = %s and bw.user_id = %s and bw.project_name = %s and bw.name = %s and bw.is_train = %s  "
        data_brain_waves = []

        data_brain_waves.append(brain_waves.org_id)
        data_brain_waves.append(brain_waves.user_id)
        data_brain_waves.append(brain_waves.project_name)
        data_brain_waves.append(brain_waves.name)
        data_brain_waves.append(brain_waves.is_train)


        if brain_waves.brain_form:
            brain_waves_sql += " and bw.brain_form = %s "
            data_brain_waves.append(brain_waves.brain_form)

        brain_waves_sql += " ORDER BY bw.create_time "


        cursor = cnx.cursor()
        result = None

        try:
            cursor.execute(brain_waves_sql, data_brain_waves)
            result = cursor.fetchall()

        except Error as e:
            result_msg = "获取一段时间脑波记录，失败"
            print(f"{result_msg}, The error '{e}' occurred")

        finally:
            if cnx.is_connected():
                cursor.close()
                cnx.close()
            return result



