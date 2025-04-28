import mysql.connector

from mysql.connector import Error, pooling

# base_db_config = {
#     "user": "nlkjuser",
#     "password": "nlkjuser",
#     "host": "localhost",
#     "database": "nlkj_base_db"
# }
base_db_config = {
    "user": "root",
    "password": "root",
    "host": "localhost",
    "database": "nlkj_base_db"
}

class MySQLConn:

    def mysql_pool(self):

        try:
            # cnx = mysql.connector.connect(pool_name="nlkj_base_pool",
            #                               pool_size=3,
            #                               **base_db_config)

            cnx = pooling.MySQLConnectionPool(pool_name="nlkj_base_db_pool",
                                              pool_size = 30,
                                              **base_db_config).get_connection()

            print('--------')


        except Error as e:
            import traceback
            traceback.print_exc()
            result_msg = "数据库服务连接失败"
            status = 10000000
            # print(f"{result_msg}，The error '{e}' occurred")
            print(f"{result_msg}，The error '{e}' occurred")

        # finally:
        return cnx


if __name__ == '__main__':
    mysql_conn = MySQLConn()
    cnx = mysql_conn.mysql_pool()
    if cnx and cnx.is_connected():

        with cnx.cursor() as cursor:

            result = cursor.execute("SELECT * FROM user_tb LIMIT 5")

            rows = cursor.fetchall()
            print(f'result:{result}')

            for rows in rows:
                print(f"rows：{rows}")

        cnx.close()


