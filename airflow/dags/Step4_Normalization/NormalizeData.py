import os

import numpy as np
from scipy import stats

from Util import commonUtil, fileUtil

APPENDIX = ['Minute', 'Hour', 'Day', 'Month', 'Year']

def zscore(data,column):
    return stats.zscore(data[column])

def rwCSV(filesAggregated:list,fileOutput:str,UserInputColumns:list,APPENDIX=APPENDIX,normalizeMethod=zscore)->list:
    files = []
    raw_output = fileOutput
    fileOutput = commonUtil.getPath(fileOutput)
    for f in filesAggregated:

        raw_name = f
        fileInput = commonUtil.getPath(f)


        data = fileUtil.readFromFileToData(fileInput)

        vals= commonUtil.d(UserInputColumns)

        for attr in UserInputColumns:
            vals[attr] = normalizeMethod(data, attr)
        # last columns is always APPENDIX, which is usually as 'Minute', 'Hour' 'Day' 'Month' 'Year'
        for attr in APPENDIX:
            vals[attr] = data[attr]

        # delete 'nan' value
        newVals = {}
        for key in vals.keys():
            if not np.isnan(vals[key][0]):
                newVals[key] = vals[key]
            else:
                newVals[key] = 0

        tmpName = raw_name.split(os.sep)[1]
        fileUtil.saveDataToCSV(fileOutput + f"_{tmpName}",newVals)
        files.append(raw_output + f"_{tmpName}")

    return files