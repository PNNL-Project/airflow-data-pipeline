# WARNING!!!
# DO NOT UPLOAD DatabaseSetting.yaml TO GITHUB!
# find it at https://drive.google.com/drive/folders/18mGDVWaXSrFJ0ikFktHV-iRB352x5PbN/

import calendar
import csv
import time
from datetime import datetime

import MySQLdb
from pytz import timezone

from Util import fileUtil, commonUtil, LoadYAML

# No print method allowed

class AWSConnection():

    def __init__(self, fileOutput, databasesetting):
        self.fileOutput = commonUtil.getPath(fileOutput)
        self.connectionInfo = LoadYAML.rDatabaseSetting(databasesetting)

        self.DATABASE_NAME = self.connectionInfo[-2]
        self.TABLE_NAME = self.connectionInfo[-1][0]

        # Sql head order will be changed
        self.head = []
        self.headString = ''

    def getConnection(self) -> MySQLdb:
        try:
            connection = MySQLdb.connect(host=self.connectionInfo[0], port=self.connectionInfo[1],
                                         user=self.connectionInfo[2], passwd=self.connectionInfo[3],
                                         database=self.connectionInfo[4],
                                         charset='utf8', connect_timeout=5)
            return connection
        except Exception as e:
            #raise(e) xing
            raise Exception("Step1 ConnectToAWS failed {}".format(e))

    def subtractHeads(self, messages):
        res = []
        for msg in messages:
            res.append(msg[0])

        self.head = res
        return ','.join(res)

    def initConnection(self):
        connection = self.getConnection()

        with connection:
            cur = connection.cursor()

            myQuery = LoadYAML.rCommonQueries('SHOWTOP1', ['*', self.TABLE_NAME])
            cur.execute(myQuery)
            msgs = cur.description
            self.headString = self.subtractHeads(msgs)

            cur.close()

    def createNewCSV(self):
        self.initConnection()
        vals = commonUtil.d(self.head)
        fileUtil.saveDataToCSV(self.fileOutput, vals)

    def previousDate(self, inputDate, myTimezone, inputFormat):
        try:
            mtz = timezone(myTimezone)
        # except Exception:
        #     #print('Please check the name of input timezone')
        #     mtz = timezone('UTC')

        except Exception as e:
            # raise(e) xing
            # raise Exception("Step1 ConnectToAWS: def previousDate failed: please check timezone input {}".format(e))
            mtz = timezone('UTC')
        utc = timezone('UTC')

        detail = time.strptime(inputDate, inputFormat)
        now_time = mtz.localize(datetime(detail.tm_year, detail.tm_mon, detail.tm_mday)) \
            .astimezone(mtz)

        timeStamp = calendar.timegm(now_time.timetuple())
        # 00:00:00 under myTimezone
        previousDayStartTimestamp = timeStamp - 24 * 3600
        # 23:59:59 under myTimezone
        previousDayEndTimestamp = timeStamp - 1

        start = datetime.utcfromtimestamp(previousDayStartTimestamp)
        end = datetime.utcfromtimestamp(previousDayEndTimestamp)

        return str(start), str(end)

    # Download Previous day data_temperature from AWS
    def loadPreviousDayData(self, inputDate, myTimezone, inputFormat):

        try:
            connection = self.getConnection()
        except Exception as e:
            # TODO
            # raise(e)
            raise Exception("Step1 ConnectToAWS: def loadPreviousDayData: self.getConnection() failed {}".format(e))

        previousStart, previousEnd = self.previousDate(inputDate, myTimezone, inputFormat)

        values = [self.headString, self.TABLE_NAME, previousStart, previousEnd]
        myQuery = LoadYAML.rCommonQueries('SELECTDATETIME', values)

        out_f = open(self.fileOutput, 'a', newline='')
        writer = csv.writer(out_f)
        try:
            with connection:
                cur = connection.cursor()
                #print(f"Start downloading")
                #print(f"Quering may take more than one minute")
                cur.execute(myQuery)
                data = cur.fetchall()
                if (not data) or len(data) == 0:
                    #print("END")
                    cur.close()
                    out_f.close()
                    raise Exception("Step1 loadPreviousDayData failed: not data")

                writer.writerows(list(data))
                cur.close()
                out_f.close()
                return previousStart.split(' ')[0]
        except Exception as e:
            raise Exception("Step1 ConnectToAWS: def loadPreviousDayData: with connection failed {}".format(e))

    def downloadPreviousDayData(self, inputDate, myTimezone='PDT', inputFormat='%Y-%m-%d %H:%M:%S'):
        self.createNewCSV()
        previousDay = self.loadPreviousDayData(inputDate, myTimezone, inputFormat)
        return previousDay

    def saveHead(self, headFile: str):
        fileUtil.saveListToCSV(headFile, self.head)