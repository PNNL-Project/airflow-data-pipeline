import sys
from datetime import datetime

from Step1_ConnectToAWS import AWSConnection
import os

def main():

    try:
        DAY = sys.argv[1]
    except Exception as e:
        #raise(e) xing
        raise Exception("Step1_ConnectToAWS failed: can't find that day {}".format(e))

    tmptime = str(datetime.strptime(DAY.split('T')[0], "%Y-%m-%d").date()) + " 0:0:1"

    try:
        databasesetting = os.path.join('Setting', 'DatabaseSetting.yaml')
    except Exception as e:
        # raise(e) xing
        raise Exception("Step1_ConnectToAWS failed: Can't find Setting or DatabaseSetting.yaml {}".format(e))

    try:
        fileOutPut = os.path.join('Tempdata'+DAY, 'srcData.csv')
    except Exception as e:
        # raise(e) xing
        raise Exception("Step1_ConnectToAWS failed: Can't find Tempdata or srcData.csv {}".format(e))

    try:
        HeadFileOutput = os.path.join('Tempdata'+DAY, 'Head')
    except Exception as e:
        # raise(e) xing
        raise Exception("Step1_ConnectToAWS failed: Can't find Tempdata or Head {}".format(e))

    try:
        connInstance = AWSConnection.AWSConnection(fileOutPut, databasesetting)
    except Exception as e:
        # raise(e) xing
        raise Exception("Step1_ConnectToAWS failed: AWSConnection failed {}".format(e))

    YESTERDAY = connInstance.downloadPreviousDayData(tmptime)
    connInstance.saveHead(HeadFileOutput)
    print(YESTERDAY)
    return YESTERDAY

if __name__ == '__main__':
    try:
        main()
        sys.exit(0)
    except Exception as e:
        print(e)
        sys.exit(1)