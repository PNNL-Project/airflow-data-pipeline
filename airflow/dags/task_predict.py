from Step2_Aggregation import Aggregation_On_Processed_Data
from Step3_ColumnSelection import PickUpColumns
from Step4_Normalization import NormalizeData
from Step5_UnitStatus import UnitStatus
from Step6_Predict import Predict
from Util import LoadYAML, commonUtil
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
        raise Exception("Can't find yesterday or name {}".format(e))

    # Step 1.5, Prepare data_temperature

    # SettingFile = os.path.join('Setting', 'input.yml')
    # HeadFileOutput = os.path.join('Tempdata', 'Head')
    try:
        SettingFile = os.path.join('Setting', 'input.yml')
    except Exception as e:
        # raise(e) xing
        raise Exception("Step 1.5 failed: cannot join Setting and input.yml {}".format(e))
    try:
        HeadFileOutput = os.path.join('Tempdata'+DAY, 'Head')
    except Exception as e:
        # raise(e) xing
        raise Exception("Step 1.5 failed: cannot join Tempdata and Head {}".format(e))

    timeIntervalList, userSelectColumns = commonUtil.getSelectedColumns(SettingFile, HeadFileOutput, NAME)
    print(userSelectColumns)
    print(timeIntervalList)

    # Step 2, Aggregate data_temperature by different intervals

    #fileInput = os.path.join('Tempdata', 'srcData.csv')
    try:
        fileInput = os.path.join('Tempdata'+DAY, 'srcData.csv')
    except Exception as e:
        # raise(e) xing
        raise Exception("Step 2 failed: cannot join Tempdata and srcData.csv {}".format(e))

    # Maybe multiple files
    # fileOutPut = os.path.join('Tempdata', NAME + '_agg_data')
    try:
        fileOutPut = os.path.join('Tempdata'+DAY, NAME + '_agg_data')
    except Exception as e:
        # raise(e) xing
        raise Exception("Step 2 failed: cannot join Tempdata，NAME and _agg_data {}".format(e))

    timeFormat = '%Y-%m-%d %H:%M:%S'
    print('Step 2, Aggregate data_temperature by different intervals')
    print("Step2 start")
    filesAggregated = Aggregation_On_Processed_Data.rwCSV(fileInput, fileOutPut, timeIntervalList=timeIntervalList,
                                                          timeFormat=timeFormat)
    print("Step2 finished")

    # Step 3, Pick up columns
    # Give different names to different selcColums

    #fileOutPut = os.path.join('Tempdata', 'selc')

    try:
        fileOutPut = os.path.join('Tempdata'+DAY, 'selc')
    except Exception as e:
        # raise(e) xing
        raise Exception("Step 3 failed: cannot join Tempdata and selc {}".format(e))

    APPENDIX = ['Minute', 'Hour', 'Day', 'Month', 'Year']
    print('Step 3, Pick up columns')
    print("Step3 start")
    filesAggregated = PickUpColumns.rwCSV(filesAggregated,
                                          fileOutPut,
                                          needColumns=userSelectColumns,
                                          Default=APPENDIX)
    print("Step3 finished")

    # Step 4, Normalize(optional to Users)
    #fileOutPut = os.path.join('Tempdata', 'norm')
    try:
        fileOutPut = os.path.join('Tempdata'+DAY, 'norm')
    except Exception as e:
        # raise(e) xing
        raise Exception("Step 4 failed: cannot join Tempdata and norm {}".format(e))

    print('Step 4, Normalize(optional to Users)')
    # Choose a normalization method, default method is Z-score
    print("Step4 start")
    filesAggregated = NormalizeData.rwCSV(filesAggregated,
                                          fileOutPut,
                                          UserInputColumns=userSelectColumns,
                                          APPENDIX=APPENDIX)
    print("Step4 finished")

    # Step 5, Do 24H UnitStatus aggregation

    #fileOutPut = os.path.join('Tempdata', NAME + '_digest.csv')
    try:
        fileOutPut = os.path.join('Tempdata'+DAY, NAME + '_digest.csv')
    except Exception as e:
        # raise(e) xing
        raise Exception("Step 5 failed: cannot join Tempdata, name and _digest.csv {}".format(e))

    timeFormat = '%M-%H-%d-%m-%Y'
    print('Step 5, Do UnitStatus aggregation')
    print("Step5 start")
    UnitStatus.rwCSV(filesAggregated,
                     fileOutPut,
                     userSelectColumns,
                     APPENDIX,
                     timeFormat, timeIntervalList)
    print("Step5 finished")

    # # Step 6, Daily data_temperature prediction
    #label_setting = os.path.join('Setting', 'ML_labels.yml')
    try:
        label_setting = os.path.join('Setting', 'ML_labels.yml')
    except Exception as e:
        # raise(e) xing
        raise Exception("Step 6 failed: cannot join Setting and ML_labels.yml {}".format(e))

    # hardcode here, in case some errors on the server
    if NAME.lower().__contains__("temp"):
        model_filepath = os.path.join('Models', 'zone_temperature_model.joblib')
        labels = LoadYAML.rSelectColumns(label_setting)['ZONETEMPERATURE']
    else:
        model_filepath = os.path.join('Models', 'zone_airflow_model.joblib')
        labels = LoadYAML.rSelectColumns(label_setting)['ZONEAIRFLOW']

    print(labels)
    prediction_filepath = os.path.join('Tempdata'+DAY, f"{NAME}_{YESTERDAY}.csv")
    print('Step 6, Daily data_temperature prediction')
    print("Step6 start")
    # prediction starts here
    Predict.prediction_flow(fileOutPut, prediction_filepath, model_filepath, labels, YESTERDAY)
    print("Step6 finished")

if __name__ == '__main__':
    try:
        main()
        sys.exit(0)
    except Exception as e:
        print(e)
        sys.exit(1)