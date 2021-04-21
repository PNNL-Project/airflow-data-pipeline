from Step7_InsertResultToDB import AddToDB
from Util import LoadYAML
import os
import sys

def main():

    # YESTERDAY = sys.argv[1]
    # NAME = sys.argv[2]
    try:
        YESTERDAY = sys.argv[1]
        NAME = sys.argv[2]
    except Exception as e:
        # raise(e) xing
        raise Exception("Can't find yesterday or name {}".format(e))

    #databasesetting = os.path.join('Setting','DatabaseSetting.yaml')
    try:
        databasesetting = os.path.join('Setting', 'DatabaseSetting.yaml')
    except Exception as e:
        # raise(e) xing
        raise Exception("Step 7 failed: cannot join Setting and DatabaseSetting.yaml {}".format(e))

    labels = ""
    #label_setting = os.path.join('Setting', 'ML_labels.yml')
    try:
        label_setting = os.path.join('Setting', 'ML_labels.yml')
    except Exception as e:
        # raise(e) xing
        raise Exception("Step 7 failed: cannot join Setting and ML_labels.yml {}".format(e))

    # hardcode here, in case some errors on the server
    if NAME.lower().__contains__("temp"):
        labels = LoadYAML.rSelectColumns(label_setting)['ZONETEMPERATURE']
    else:
        labels = LoadYAML.rSelectColumns(label_setting)['ZONEAIRFLOW']

    print('Step 8, save failure result back to AWS')
    print("Step8 start")

    # connInstance = AddToDB.AWSConnection(databasesetting,NAME)
    # connInstance.finsert(labels,YESTERDAY)

    try:
        connInstance = AddToDB.AWSConnection(databasesetting, NAME)
        connInstance.finsert(labels, YESTERDAY)
    except Exception as e:
        # raise(e) xing
        raise Exception("Step 8 failed: fail to insert to db {}".format(e))

    print("Step8 finished")

if __name__ == '__main__':
    try:
        main()
        sys.exit(0)
    except Exception as e:
        print(e)
        sys.exit(1)