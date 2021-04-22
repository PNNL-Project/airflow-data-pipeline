import os
import re

from Util import commonUtil
from Util import fileUtil

flag_ignore = re.IGNORECASE
# Head = 'Head.txt'
Default = ['Hour', 'Day', 'Month', 'Year']
Head = 'Head'


def rwCSV(filesAggregated: list, fileOutput: str, needColumns: list, Default: list, pivot='datetime') -> list:

    files = []
    raw_output = fileOutput
    fileOutput = commonUtil.getPath(fileOutput)
    for f in filesAggregated:

        raw_name = f
        fileInput = commonUtil.getPath(f)

        data = fileUtil.readFromFileToData(fileInput=fileInput)
        # Default columns in the last columns
        vals = commonUtil.d(needColumns, Default)
        for attr in needColumns + Default:
            vals[attr] = data[attr]

        tmpName = raw_name.split(os.sep)[1]

        # Lost Order
        fileUtil.saveDataToCSV(fileOutput + f"_{tmpName}", vals)
        files.append(raw_output + f"_{tmpName}")

    return files
