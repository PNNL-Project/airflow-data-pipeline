from Step7_InsertResultToDB import AddToDB
from Util import fileUtil
import os
import sys

def main():

    # YESTERDAY = sys.argv[1]
    # NAME = sys.argv[2]
    try:
        YESTERDAY = sys.argv[1]
        NAME = sys.argv[2]
        DAY = sys.argv[3]
    except Exception as e:
        # raise(e) xing
        raise Exception("Step7_InsertResultToDB failed: Can't find yesterday or name {}".format(e))

    # databasesetting = os.path.join('Setting','DatabaseSetting.yaml')
    try:
        databasesetting = os.path.join('Setting','DatabaseSetting.yaml')
    except Exception as e:
        # raise(e) xing
        raise Exception("Step7_InsertResultToDB failed: Can't join Setting and DatabaseSetting.yaml {}".format(e))

    # prediction_filepath = os.path.join('Tempdata', f"{NAME}_{YESTERDAY}.csv")
    try:
        prediction_filepath = os.path.join('Tempdata'+DAY, f"{NAME}_{YESTERDAY}.csv")
    except Exception as e:
        # raise(e) xing
        raise Exception("Step7_InsertResultToDB failed: Can't join Tempdata and file yesterday csv {}".format(e))

    print('Step 7, save prediction back to AWS')
    print("Step7 start")

    # connInstance = AddToDB.AWSConnection(databasesetting,NAME)
    try:
        connInstance = AddToDB.AWSConnection(databasesetting, NAME)
    except Exception as e:
        # raise(e) xing
        raise Exception("Step7_InsertResultToDB failed: AddToDB.AWSConnection failed {}".format(e))

    data = fileUtil.readFromFileToListWithoutHead(prediction_filepath)
    print(data)

    #connInstance.insert(data)
    try:
        connInstance.insert(data)
    except Exception as e:
        # raise(e) xing
        raise Exception("Step7_InsertResultToDB failed: connInstance.insert(data) failed {}".format(e))

    print("Step7 finished")

if __name__ == '__main__':
    try:
        main()
        sys.exit(0)
    except Exception as e:
        print(e)
        sys.exit(1)