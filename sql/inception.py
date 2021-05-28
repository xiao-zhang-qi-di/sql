import MySQLdb
from django.conf import settings


class InceptionDao(object):
    def __init__(self):
        try:
            self.INCEPTION_HOST = getattr(settings, 'INCEPTION_HOST')
            self.INCEPTION_PORT = getattr(settings, 'INCEPTION_PORT')
        except AttributeError as e:
            print("Error:%s" % e)
            quit(1)

    def sqlautoReview(self, sql_content, cluster_name):
        sql = '/*--user=username;--password=password;--host=127.0.0.1;--execute=1;--port=3306;*/\
        inception_magic_start;\
        use mysql;\
        CREATE TABLE adaptive_office(id int);\
        inception_magic_commit;'
        try:
            conn = MySQLdb.connect(host='127.0.0.1', user='', passwd='', db='', port=9998)
            cur = conn.cursor()
            ret = cur.execute(sql)
            result = cur.fetchall()
            num_fields = len(cur.description)
            field_names = [i[0] for i in cur.description]
            print(field_names)
            for row in result:
                print(row[0], "|", row[1], "|", row[2], "|", row[3], "|", row[4], "|",
                      row[5], "|", row[6], "|", row[7], "|", row[8], "|", row[9], "|", row[10])
            cur.close()
            conn.close()
        except MySQLdb.Error as e:
            print("Mysql Error %d: %s" % (e.args[0], e.args[1]))
