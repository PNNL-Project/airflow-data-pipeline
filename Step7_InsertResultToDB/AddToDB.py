from datetime import datetime
from Util import LoadYAML
import MySQLdb


class AWSConnection():

    def __init__(self,  databasesetting:str,NAME:str):
        self.connectionInfo = LoadYAML.rDatabaseSetting(databasesetting)
        self.DATABASE_NAME = self.connectionInfo[-2]
        self.TABLE_NAME = ""
        for tidx,tname in enumerate(self.connectionInfo[-1]):
            if tname[0:6].lower().__contains__(NAME.lower()[0:6]):
                self.TABLE_NAME = self.connectionInfo[-1][tidx]
                break

    def getConnection(self) -> MySQLdb:


        connection = MySQLdb.connect(host=self.connectionInfo[0], port=self.connectionInfo[1],
                                     user=self.connectionInfo[2], passwd=self.connectionInfo[3],
                                     database=self.connectionInfo[4],
                                     charset='utf8')
        return connection

    def insert(self,data:list):
        try:
            connection = self.getConnection()
        except:
            raise("Connection failed!")

        myQuery = LoadYAML.rCommonQueries('INSERT',
                                          [self.TABLE_NAME,
                                           '`Date`, `Label`, `Frequency`',
                                           '%s, %s, %s'])

        with connection:
            cur = connection.cursor()
            for line in data:
                valuesData = self.getElements(line)
                try:
                    cur.execute(myQuery,valuesData)
                except Exception as e:
                    connection.rollback()
                    cur.close()
                    raise(e)
            cur.close()
            connection.commit()

    def finsert(self,labels:list,YERSTERDAY:str):
        try:
            connection = self.getConnection()
        except Exception as e:
            raise(e)

        data = []
        time = self.getDate(YERSTERDAY)
        for label in labels:
            data.append((time,label,-1))

        myQuery = LoadYAML.rCommonQueries('INSERT',
                                          [self.TABLE_NAME,
                                           '`Date`, `Label`, `Frequency`',
                                           '%s, %s, %s'])

        with connection:
            cur = connection.cursor()
            for line in data:
                try:
                    cur.execute(myQuery,line)
                except Exception as e:
                    connection.rollback()
                    cur.close()
                    raise(e)
            cur.close()
            connection.commit()

    def getDate(self,value):
        value = value.strip()
        return datetime.strptime(value, "%Y-%m-%d").date()

    def getElements(self,line):

        line = line.strip().split(',')

        date = self.getDate(line[0])
        label = line[1]
        frequency = int(line[2])
        return date, label, frequency