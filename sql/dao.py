import MySQLdb

class Dao(object):
    # 连进指定的mysql实例里, 读取所有database并返回
    def getAlldbByCluster(self, masterHost, masterPort, masterUser, masterPassword):
        listDb = []
        conn = None
        cursor = None

        try:
            conn = MySQLdb.connect(host=masterHost, port=masterPort, user=masterUser, passwd=masterPassword, charset='utf8mb4')
            cursor = conn.cursor()
            sql = "show databases"
            n = cursor.execute(sql)     # n: 多少个数据库
            # print(n)
            listDb = [row[0] for row in cursor.fetchall() if row[0] not in ('information_schema', 'performance_schema', 'mysql', 'test', 'djangoDoc', 'meiduo_mall', 'newtest', 'school', 'sys', 'test1')]
            # print(listDb)
        except MySQLdb.Warning as w:
            print(str(w))
        except MySQLdb.Error as e:
            print(str(e))
        finally:
            if cursor is not None:
                cursor.close()
            if conn is not None:
                conn.commit()
                conn.close()
        return listDb
