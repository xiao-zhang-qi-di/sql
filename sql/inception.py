# -*-coding: utf-8-*-

import re
import json
import MySQLdb
from django.conf import settings

from .models import master_config, workflow


class InceptionDao(object):
    def __init__(self):
        try:
            self.inception_host = getattr(settings, 'INCEPTION_HOST')
            self.inception_port = int(getattr(settings, 'INCEPTION_PORT'))

            self.inception_remote_backup_host = getattr(settings, 'INCEPTION_REMOTE_BACKUP_HOST')
            self.inception_remote_backup_port = int(getattr(settings, 'INCEPTION_REMOTE_BACKUP_PORT'))
            self.inception_remote_backup_user = getattr(settings, 'INCEPTION_REMOTE_BACKUP_USER')
            self.inception_remote_backup_password = getattr(settings, 'INCEPTION_REMOTE_BACKUP_PASSWORD')
        except AttributeError as a:
            print("Error: %s" % a)
        except ValueError as v:
            print("Error: %s" % v)

    def sqlautoReview(self, sqlContent, clusterName, isbackup):
        '''
        将sql交给inception进行自动审核，并返回审核结果。
        '''
        listMasters = master_config.objects.filter(cluster_name=clusterName)
        if len(listMasters) != 1:
            print("Error: 主库配置返回为0")
        masterHost = listMasters[0].master_host
        masterPort = listMasters[0].master_port
        masterUser = listMasters[0].master_user
        masterPassword = listMasters[0].master_password

        # 这里无需判断字符串是否以；结尾，直接抛给inception enable check即可。
        # if sqlContent[-1] != ";":
        # sqlContent = sqlContent + ";"

        # sql = "/*--user=%s;--password=%s;--host=%s;--enable-check=1;--port=%s;*/\
        #   inception_magic_start;\
        #   %s\
        #   inception_magic_commit;" % (masterUser, masterPassword, masterHost, str(masterPort), sqlContent)
        sql = sqlContent
        # result = self._fetchall(sql, self.inception_host, self.inception_port, '', '', '')
        result = self._fetchall(sql, masterHost, masterPort, masterUser, masterPassword, 'sql')
        return result

    def executeFinal(self, workflowDetail, dictConn):
        '''
        将sql交给inception进行最终执行，并返回执行结果。
        '''
        strBackup = ""
        if workflowDetail.is_backup == '是':
            strBackup = "--enable-remote-backup;"
        else:
            strBackup = "--disable-remote-backup;"

        # 根据inception的要求，执行之前最好先split一下
        sqlSplit = "/*--user=%s; --password=%s; --host=%s; --enable-execute;--port=%s; --enable-ignore-warnings;--enable-split;*/\
             inception_magic_start;\
             %s\
             inception_magic_commit;" % (
        dictConn['masterUser'], dictConn['masterPassword'], dictConn['masterHost'], str(dictConn['masterPort']),
        workflowDetail.sql_content)
        splitResult = self._fetchall(sqlSplit, self.inception_host, self.inception_port, '', '', '')

        tmpList = []
        # 对于split好的结果，再次交给inception执行.这里无需保持在长连接里执行，短连接即可.
        for splitRow in splitResult:
            sqlTmp = splitRow[1]
            sqlExecute = "/*--user=%s;--password=%s;--host=%s;--enable-execute;--port=%s; --enable-ignore-warnings;%s*/\
                    inception_magic_start;\
                    %s\
                    inception_magic_commit;" % (
            dictConn['masterUser'], dictConn['masterPassword'], dictConn['masterHost'], str(dictConn['masterPort']),
            strBackup, sqlTmp)

            executeResult = self._fetchall(sqlExecute, self.inception_host, self.inception_port, '', '', '')
            tmpList.append(executeResult)

        # 二次加工一下，目的是为了和sqlautoReview()函数的return保持格式一致，便于在detail页面渲染.
        finalStatus = "已正常结束"
        finalList = []
        for splitRow in tmpList:
            for sqlRow in splitRow:
                # 如果发现任何一个行执行结果里有errLevel为1或2，并且stagestatus列没有包含Execute Successfully字样，则判断最终执行结果为有异常.
                if (sqlRow[2] == 1 or sqlRow[2] == 2) and re.match(r"\w*Execute Successfully\w*", sqlRow[3]) is None:
                    finalStatus = "执行有异常"
                finalList.append(list(sqlRow))

        return (finalStatus, finalList)

    def getRollbackSqlList(self, workflowId):
        workflowDetail = workflow.objects.get(id=workflowId)
        listExecuteResult = json.loads(workflowDetail.execute_result)
        listBackupSql = []
        for row in listExecuteResult:
            # 获取backup_dbname
            if row[8] == 'None':
                continue;
            backupDbName = row[8]
            sequence = row[7]
            opidTime = sequence.replace("'", "")
            sqlTable = "select tablename from %s.$_$Inception_backup_information$_$ where opid_time='%s';" % (
            backupDbName, opidTime)
            listTables = self._fetchall(sqlTable, self.inception_remote_backup_host, self.inception_remote_backup_port,
                                        self.inception_remote_backup_user, self.inception_remote_backup_password, '')
            if listTables is None or len(listTables) != 1:
                print("Error: returned listTables more than 1.")

            tableName = listTables[0][0]
            sqlBack = "select rollback_statement from %s.%s where opid_time='%s'" % (backupDbName, tableName, opidTime)
            listBackup = self._fetchall(sqlBack, self.inception_remote_backup_host, self.inception_remote_backup_port,
                                        self.inception_remote_backup_user, self.inception_remote_backup_password, '')
            if listBackup is not None and len(listBackup) != 0:
                listBackupSql.append(listBackup[0][0])
        return listBackupSql

    def _fetchall(self, sql, paramHost, paramPort, paramUser, paramPasswd, paramDb):
        '''
        封装mysql连接和获取结果集方法
        '''
        result = None
        conn = None
        cur = None
        try:
            conn = MySQLdb.connect(host=paramHost, user=paramUser, passwd=paramPasswd, db=paramDb, port=paramPort)
            cur = conn.cursor()
            ret = cur.execute(sql)
            result = cur.fetchall()
        except MySQLdb.Error as e:
            print("Mysql Error %d: %s" % (e.args[0], e.args[1]))
        finally:
            cur.close()
            conn.close()
        return result

